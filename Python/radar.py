import serial
import pygame
import math
import sys

# ----------------- CONFIG -----------------
PORT = "COM3"  # <-- CHANGE THIS to your Arduino port if needed
BAUDRATE = 9600
MAX_DISTANCE_CM = 100  # must match Arduino
# ------------------------------------------

# Init serial
try:
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
except Exception as e:
    print("Could not open serial port:", e)
    sys.exit(1)

# Tell Arduino to START (servoEnabled = true)
try:
    ser.write(b'1')
except Exception as e:
    print("Warning: could not send start command:", e)

# Init pygame
pygame.init()
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arduino Radar")

clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 18)

# Radar origin (bottom center)
origin_x = WIDTH // 2
origin_y = HEIGHT - 20
max_radius_px = 300  # max range on screen in pixels

current_angle_deg = 90
current_distance = MAX_DISTANCE_CM
running_servo = True  # we start in RUNNING mode


def draw_radar_base():
    screen.fill((0, 0, 0))

    # Draw arcs (range circles)
    for r in range(100, max_radius_px + 1, 50):
        pygame.draw.arc(
            screen,
            (0, 255, 0),
            (origin_x - r, origin_y - r, 2 * r, 2 * r),
            math.pi,
            2 * math.pi,
            1,
        )

    # Draw angle lines
    for a in range(15, 166, 15):
        rad = math.radians(a)
        x = origin_x + math.cos(rad) * max_radius_px
        y = origin_y - math.sin(rad) * max_radius_px
        pygame.draw.line(screen, (0, 255, 0), (origin_x, origin_y), (x, y), 1)


def draw_sweep_and_point(angle_deg, distance_cm):
    # Limit distance
    if distance_cm > MAX_DISTANCE_CM:
        distance_cm = MAX_DISTANCE_CM

    # Convert angle to radians
    rad = math.radians(angle_deg)

    # Sweep line (still full radius)
    sx = origin_x + math.cos(rad) * max_radius_px
    sy = origin_y - math.sin(rad) * max_radius_px
    pygame.draw.line(screen, (0, 255, 0), (origin_x, origin_y), (sx, sy), 2)

    # --- Better scaling for the dot ---
    # Even very close objects shouldn't be exactly at the root,
    # so we define a minimum radius.
    min_r = 40  # pixels
    # Scale distance into [min_r, max_radius_px]
    r = min_r + (distance_cm / MAX_DISTANCE_CM) * (max_radius_px - min_r)

    px = origin_x + math.cos(rad) * r
    py = origin_y - math.sin(rad) * r

    # Draw dot only if something is in range
    if distance_cm < MAX_DISTANCE_CM:
        # 🔴 Detection dot in RED now
        pygame.draw.circle(screen, (255, 0, 0), (int(px), int(py)), 6)


def read_serial_line():
    if ser.in_waiting > 0:
        try:
            line = ser.readline().decode("utf-8").strip()
        except UnicodeDecodeError:
            return None, None

        if not line:
            return None, None

        parts = line.split(",")
        if len(parts) != 2:
            return None, None

        try:
            angle = float(parts[0])
            distance = float(parts[1])
            return angle, distance
        except ValueError:
            return None, None

    return None, None


def draw_status(running_servo, current_distance):
    # Status text: RUNNING / STOPPED and last distance
    status_text = "STATUS: RUNNING (S = toggle)" if running_servo else "STATUS: STOPPED (S = toggle)"
    dist_text = f"Distance: {current_distance:.1f} cm"

    status_surf = font.render(status_text, True, (0, 255, 0) if running_servo else (255, 0, 0))
    dist_surf = font.render(dist_text, True, (0, 255, 0))

    screen.blit(status_surf, (10, 10))
    screen.blit(dist_surf, (10, 35))


# --------------- MAIN LOOP ----------------
running = True
while running:
    clock.tick(30)  # 30 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                # Toggle servo on/off
                running_servo = not running_servo
                try:
                    if running_servo:
                        ser.write(b'1')   # start
                        print("Servo START")
                    else:
                        ser.write(b'0')   # stop
                        print("Servo STOP")
                except Exception as e:
                    print("Serial write error:", e)

    # Try to read one line from Arduino
    angle, dist = read_serial_line()
    if angle is not None and dist is not None:
        current_angle_deg = angle
        current_distance = dist

    # Draw radar
    draw_radar_base()
    draw_sweep_and_point(current_angle_deg, current_distance)
    draw_status(running_servo, current_distance)

    pygame.display.flip()

# Cleanup
ser.close()
pygame.quit()
sys.exit()
