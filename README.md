# RS485 Stepper Motor Driver

[![Python CI](https://github.com/Simon2022s/RS485-Stepper-Motor-Driver/actions/workflows/python-ci.yml/badge.svg)](https://github.com/Simon2022s/RS485-Stepper-Motor-Driver/actions/workflows/python-ci.yml)

A PyQt5-based RS485 stepper motor driver control software with Modbus RTU protocol support. Originally designed for the [AR28 closed-loop stepper motor driver](https://www.adampower.de/nema11-rs485-stepper-motor-driver), compatible with similar Modbus RTU devices.

![AR28 Driver](bruce_bg.jpg)

## 🚀 Features

- **Serial Communication**: RS485 serial communication with automatic port detection
- **Motor Control**: Speed, acceleration, deceleration, and position control
- **Parameter Settings**: Current, PPR (pulses per revolution), and direction settings
- **Real-time Monitoring**: Real-time query of speed, position, and current
- **Motion Modes**: Continuous motion, incremental positioning, and absolute positioning
- **Data Logging**: Command sending and receiving log support
- **Beautiful UI**: Bruce Lee themed UI design

## 📋 System Requirements

- Python 3.8+
- Windows / Linux / macOS
- RS485 to USB adapter

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Simon2022s/RS485-Stepper-Motor-Driver.git
cd RS485-Stepper-Motor-Driver
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### 3. Install Dependencies

**Method A: Using Launcher with Auto-Installation (Recommended)**

Windows users can simply double-click:
```
start.bat
```

Or use the Python launcher:
```bash
python run.py
```
The launcher will automatically check and install missing dependencies.

**Method B: Manual Installation**

```bash
pip install -r requirements.txt
```

Or install only core dependencies:
```bash
pip install PyQt5>=5.15.0 pyserial>=3.5
```

## 🎮 Usage

### Run the Program

**Method 1: Using Launcher (Auto-check Dependencies)**
```bash
# Windows
start.bat

# Or
python run.py
```

**Method 2: Direct Run**
```bash
python BruceLee.py
```

**Note**: If running `python BruceLee.py` shows missing PyQt5 or pyserial errors, please install dependencies first:
```bash
pip install PyQt5 pyserial
```

### Basic Operations

1. **Connect Serial Port**: Click "Serial Setup" to configure port parameters, then click "Open"
2. **Set Motor ID**: Enter motor address in the Motor ID input box (default: 1)
3. **Set Parameters**: 
   - Speed: Set target speed (pulses/second)
   - Acceleration: Set acceleration value
   - Deceleration: Set deceleration value
4. **Control Motor**:
   - Enable: Enable the motor
   - ▶▶: Forward continuous motion
   - ◀◀: Reverse continuous motion
   - ||: Pause
   - Disable: Disable the motor

### Advanced Features

- **Custom Commands**: Enter Modbus commands directly in the Hex Command area
- **Query Function**: Use 🔍 button to query current parameter values
- **Save Parameters**: Click Save to store parameters to motor EEPROM

## 📁 Project Structure

```
RS485-Stepper-Motor-Driver/
├── BruceLee.py              # Main program entry
├── run.py                   # Auto-install dependencies and launch
├── start.bat                # Windows one-click launcher
├── longgeforeverUI.py       # Main UI interface
├── rsNew.py                 # Serial port settings dialog UI
├── system.py                # System settings module
├── sendRes.py               # Serial communication thread
├── crc.py                   # CRC16 checksum
├── readIni.py               # Configuration file reader
├── public.py                # Global variables
├── log.py                   # Logging module
├── system.ini               # Configuration file
├── bruce_bg.jpg             # Background image
├── logo.ico                 # Application icon
├── wu.ico                   # Window icon
├── requirements.txt         # Dependency list
├── setup.cfg                # pytest configuration
├── CODE_REVIEW.md           # Code review report
├── CI_FIXES.md              # CI fixes record
├── optimized_example.py     # Optimized code example
└── tests/                   # Unit test directory
    ├── __init__.py
    └── test_crc.py
```

## 🔌 Communication Protocol

This software uses **Modbus RTU** protocol to communicate with motor drivers.

### Common Registers

| Register Address | Function | Description |
|-----------------|----------|-------------|
| 0x0000 | Current | Read/Set current |
| 0x0001 | PPR | Pulses per revolution |
| 0x0003 | Standby Current | Standby current percentage |
| 0x001A | Peak Current | Peak current percentage |
| 0x0040 | Speed Low | Speed value low 16 bits |
| 0x0041 | Speed High | Speed value high 16 bits |
| 0x0042 | Acceleration Low | Acceleration low 16 bits |
| 0x0043 | Acceleration High | Acceleration high 16 bits |
| 0x0044 | Position Low | Position value low 16 bits |
| 0x0045 | Position High | Position value high 16 bits |
| 0x0046 | Control Mode | Start/Stop/Direction control |
| 0x0048 | Position Mode | Incremental/Absolute mode |

### CRC Checksum

Uses standard Modbus RTU CRC16 checksum algorithm.

## 🛠️ Development

### Code Standards

- Follow PEP 8 code style
- Use type annotations
- Write docstrings

### Run Tests

```bash
pytest
```

### Code Checking

```bash
# Code style check
flake8 .

# Type check
mypy .

# Security check
bandit -r .
```

## 📦 Packaging

Package as executable using PyInstaller:

```bash
pyinstaller --onefile --windowed --icon=logo.ico BruceLee.py
```

## 📝 Changelog

### v1.0.0 (2026-03-09)
- ✨ Initial release
- 🎨 Bruce Lee themed UI
- 🔧 AR28 driver support
- 📊 Real-time parameter query

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 📄 License

MIT License

## 🙏 Acknowledgments

- PyQt5 - GUI framework
- pySerial - Serial communication library
- [Adam Power](https://www.adampower.de/nema11-rs485-stepper-motor-driver) - AR28 stepper motor driver reference design

---

**Note**: This software is for learning and testing purposes only. Please test thoroughly before using in industrial environments.
