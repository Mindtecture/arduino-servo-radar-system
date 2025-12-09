# Arduino Servo Radar System 📡

A complete real-time radar system using:

- Arduino UNO / Nano
- SG90 Micro Servo
- HC-SR04 Ultrasonic Sensor
- Red & Green LEDs
- Python + Pygame Visualization
- Serial Start/Stop Control

This project demonstrates full **hardware + firmware + software integration**.

---

## 🔧 Hardware Components

- Arduino UNO / Nano
- SG90 Servo Motor
- HC-SR04 Ultrasonic Sensor
- 2x LEDs
- 2x 220Ω Resistors
- Breadboard & Jumper Wires

---

## 🔌 Pin Connections

| Part         | Arduino Pin |
| ------------ | ----------- |
| Servo Signal | D9          |
| HC-SR04 TRIG | D10         |
| HC-SR04 ECHO | D11         |
| Red LED      | D6          |
| Green LED    | D7          |
| Power        | 5V          |
| Ground       | GND         |

---

## 🧠 Features

- Real-time distance scanning
- LED object indication
- Python radar visualization
- Keyboard-controlled start/stop
- Scaled radar for close-range detection

---

## 🐍 Python Requirements

This project works with **any modern Python version (3.9+)**, including **Python 3.14**.

Install the required libraries using:

```bash
pip install pyserial pygame
```

## ▶️ How to Run

1. Upload the Arduino sketch from the `Arduino/` folder to your Arduino board.
2. Connect the Arduino via USB.
3. Run the Python radar visualizer:

```bash
python Python/radar.py
```

4. Press **S** in the radar window to toggle **START / STOP**.

### 🎓 Educational Use

This project is suitable for:

- Pre-university robotics students
- Engineering freshmen
- Mechatronics and embedded systems courses

---

## 📜 License

MIT License — Free to use and modify.
