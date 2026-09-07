[Arduino Ultrasonic Radar – README.md](https://github.com/user-attachments/files/31917459/Arduino.Ultrasonic.Radar.README.md)
# 🔴 Arduino Ultrasonic Radar

A real-time ultrasonic radar system built using an **Arduino UNO**, **HC-SR04 ultrasonic sensor**, **SG90 servo motor**, and **Python Matplotlib**.

The ultrasonic sensor is mounted on the servo motor and scans an area from **0° to 90°**. The measured angle and distance are transmitted from the Arduino to a Python application through USB Serial communication. The Python application displays the detected object on a radar-style graphical interface.

---

## 📌 Features

- 📡 HC-SR04 ultrasonic distance measurement
- 🔄 Automatic servo scanning
- 📐 0°–90° scanning angle
- 📏 Distance measurement from approximately 2 cm up to 2 m
- 💻 Real-time Python radar visualization
- 🔴 Object detection bubble
- 📍 Displays detected object's:
  - Distance
  - Angle
- 📊 Radar distance scale: 10 cm, 20 cm, 30 cm ... 200 cm
- 🔌 Arduino-to-PC Serial communication
- ⚡ 115200 baud rate

---

# 🛠️ Hardware Requirements

| Component | Quantity | Purpose |
|---|---:|---|
| Arduino UNO | 1 | Main microcontroller |
| HC-SR04 Ultrasonic Sensor | 1 | Distance measurement |
| SG90 Servo Motor | 1 | Rotates the ultrasonic sensor |
| Breadboard | 1 | Circuit prototyping |
| Jumper Wires | Several | Connections |
| USB Cable | 1 | Arduino programming & Serial communication |
| Computer/Laptop | 1 | Python radar visualization |

---

# 🔌 Hardware Connections

## HC-SR04 → Arduino UNO

| HC-SR04 Pin | Arduino UNO |
|---|---|
| VCC | 5V |
| GND | GND |
| TRIG | D7 |
| ECHO | D8 |

## SG90 Servo → Arduino UNO

| Servo Wire | Arduino |
|---|---|
| Brown / Black | GND |
| Red | 5V |
| Orange / Yellow | D9 |

### Complete Connection

```text
              Arduino UNO
           ┌───────────────┐
           │               │
      5V ──┤───────────────┼──── HC-SR04 VCC
     GND ──┤───────────────┼──── HC-SR04 GND
      D7 ──┤───────────────┼──── HC-SR04 TRIG
      D8 ──┤───────────────┼──── HC-SR04 ECHO
           │               │
      D9 ──┤───────────────┼──── Servo Signal
           │               │
           └───────────────┘

Servo:
Red       → 5V
Brown     → GND
Orange    → D9
```

> ⚠️ Make sure the HC-SR04 **TRIG and ECHO pins are not swapped**.

---

# 📐 Radar Configuration

The current radar configuration is:

```text
Minimum Distance : 2 cm
Maximum Distance : 200 cm

Minimum Angle    : 0°
Maximum Angle    : 90°
```

The servo continuously scans:

```text
0° → 90° → 0°
```

During the scan, the Arduino measures the distance at different angles.

---

# 💻 Software Requirements

## Arduino

Install:

- Arduino IDE
- Servo library

The Arduino sends measurements to the computer through Serial:

```text
angle,distance
```

Example:

```text
0,35.4
10,34.8
20,32.7
30,31.9
40,30.5
```

---

# 🐍 Python Requirements

Python is used to create the radar display.

Required packages:

```bash
pip install pyserial matplotlib numpy
```

Check Python:

```bash
python --version
```

Check pip:

```bash
pip --version
```

---

# 📂 Project Structure

Recommended project structure:

```text
Arduino-Ultrasonic-Radar/
│
├── Arduino/
│   └── ultrasonic_radar.ino
│
├── Python/
│   └── radar.py
│
├── README.md
│
└── images/
    └── hardware_setup.jpg
```

---

# ⚙️ Arduino Setup

### 1. Connect the hardware

Connect the HC-SR04 and servo according to the wiring table above.

### 2. Connect Arduino UNO

Connect the Arduino to the computer using a USB cable.

### 3. Open Arduino IDE

Open:

```text
Arduino/ultrasonic_radar.ino
```

### 4. Select Board

```text
Tools → Board → Arduino UNO
```

### 5. Select COM Port

```text
Tools → Port → COMx
```

For example:

```text
COM4
```

### 6. Upload the code

Click:

```text
Upload
```

---

# 🐍 Python Setup

Install the required libraries:

```bash
pip install pyserial matplotlib numpy
```

Then open:

```text
Python/radar.py
```

Make sure the COM port matches your Arduino.

Example:

```python
PORT = "COM4"
BAUD_RATE = 115200
```

If your Arduino is connected to another port, change `COM4`.

For example:

```python
PORT = "COM5"
```

---

# ▶️ Running the Radar

First upload the Arduino code.

Then close the Arduino Serial Monitor.

> ⚠️ The Arduino Serial Monitor and Python program should not normally use the same Serial port at the same time.

Run:

```bash
python radar.py
```

The Python radar window should open.

---

# 🎯 Radar Display

The radar display shows:

```text
              90°
               |
               |
          🔴 OBJECT
               |
               |
0° ────────────┴────────────
```

The red detection bubble represents the detected object.

The information label displays:

```text
Distance: 35.4 cm
Angle: 40°
```

The radar scale is:

```text
10 cm
20 cm
30 cm
40 cm
...
200 cm
```

---

# 📡 How It Works

The system operates in several stages.

### 1. Servo Positioning

The Arduino moves the servo to a specific angle.

```text
0°
10°
20°
30°
...
90°
```

### 2. Ultrasonic Measurement

The HC-SR04 sends an ultrasonic pulse.

The sound wave reflects from an object and returns to the sensor.

The Arduino measures the echo time.

### 3. Distance Calculation

The approximate distance is calculated using:

```text
Distance = Echo Time × Speed of Sound / 2
```

The division by 2 is required because the sound travels:

```text
Sensor → Object
Object → Sensor
```

### 4. Serial Transmission

Arduino sends:

```text
angle,distance
```

to the computer.

Example:

```text
45,32.6
```

### 5. Python Visualization

Python receives the data and converts the angle and distance into polar coordinates.

The object is then displayed as a red bubble.

---

# 🧪 Testing the HC-SR04

Before running the complete radar system, test the ultrasonic sensor separately.

A test target can be placed approximately:

```text
30 cm
```

from the sensor.

The Serial Monitor should show a value close to the actual distance.

For example:

```text
Distance: 29.8 cm
Distance: 30.2 cm
Distance: 30.0 cm
```

Small variations are normal.

---

# ⚠️ Troubleshooting

## 1. Radar window opens but no object appears

Check:

- Arduino COM port
- Python COM port
- USB cable
- Baud rate
- Arduino Serial output
- Python Serial connection

The baud rate must match:

```text
Arduino : 115200
Python  : 115200
```

---

## 2. Distance is completely wrong

Check the HC-SR04 wiring carefully.

```text
VCC  → 5V
GND  → GND
TRIG → D7
ECHO → D8
```

Especially check that:

```text
TRIG ≠ ECHO
```

---

## 3. Sensor gives random values

Possible causes:

- Loose jumper wires
- Incorrect power connection
- Floating ECHO pin
- Object is too close
- Object has an unsuitable surface
- Electrical noise
- Sensor damaged

Test the HC-SR04 independently before debugging the Python radar.

---

## 4. Servo does not move

Check:

```text
Servo Signal → D9
Servo VCC    → 5V
Servo GND    → GND
```

If the servo causes Arduino resets or unstable readings, use an appropriate external 5V supply for the servo and **connect the external supply GND to Arduino GND**.

---

## 5. Python says COM port is unavailable

Example error:

```text
SerialException: could not open port 'COM4'
```

Check Windows:

```text
Device Manager
    ↓
Ports (COM & LPT)
    ↓
Arduino
```

Then update:

```python
PORT = "COMx"
```

with the correct COM port.

Also close Arduino Serial Monitor before starting Python.

---

# ⚠️ Important Accuracy Note

The **2 m setting is the maximum display/measurement range configured in the software**. It does not automatically make the HC-SR04 accurate to 2 m.

The HC-SR04's practical accuracy depends on:

- Target surface
- Target angle
- Sensor orientation
- Environmental conditions
- Wiring
- Power supply
- Sensor quality

For accurate operation, always compare the sensor reading with a known physical distance during testing.

---

# 🚀 Future Improvements

Possible upgrades:

- 🔵 Multiple object detection
- 🎨 Improved radar graphics
- 📈 Distance history
- 🔔 Buzzer when an object is detected
- 📱 Web-based radar display
- 📡 ESP32 wireless version
- 💾 Data logging
- 🎯 Better filtering
- 🔄 Wider scanning angle
- 📷 Camera + ultrasonic sensor integration
- 🤖 Automatic object tracking

---

# 👨‍💻 Project

**Arduino Ultrasonic Radar**

Hardware:

```text
Arduino UNO
HC-SR04
SG90 Servo
```

Software:

```text
Arduino C/C++
Python
NumPy
Matplotlib
PySerial
```

Communication:

```text
USB Serial
115200 baud
```

Scanning:

```text
0° – 90°
```

Maximum configured range:

```text
200 cm
```

---

## 📜 License

This project is intended for educational and experimental purposes.
