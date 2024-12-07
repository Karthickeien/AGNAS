# AGNAS - Automated Guidance and Navigation for Aerial Systems

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.7+-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.5+-green?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)
[![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-4B-red?style=for-the-badge&logo=raspberry-pi&logoColor=white)](https://www.raspberrypi.org/)
[![Computer Vision](https://img.shields.io/badge/CV-Computer%20Vision-blue?style=for-the-badge&logo=opencv&logoColor=white)](https://github.com/topics/computer-vision)
[![Drone](https://img.shields.io/badge/Drone-Automation-brightgreen?style=for-the-badge&logo=drone&logoColor=white)](https://github.com/topics/drone)

## Project Overview
This project implements an autonomous drone system using a KK flight controller and Raspberry Pi 4, capable of computer vision-based navigation and package manipulation using ArUco markers. The system demonstrates advanced capabilities in autonomous flight, object detection, and precise package handling.

## Features
- **Flight Control**: Utilizes KK flight controller for stable hovering and navigation
- **Computer Vision**: Implements real-time vision processing for navigation and marker detection
- **ArUco Marker Detection**: Enables precise identification of pickup/delivery locations
- **Electromagnetic Gripper**: Features an electromagnet for versatile package handling
- **Autonomous Navigation**: Supports predefined waypoint navigation and bin delivery
- **Altitude Hold**: Maintains stable height during flight operations
- **Fail-Safe Mechanisms**: Includes signal loss detection and safe landing procedures
- **RC Signal Processing**: Advanced PWM signal handling for both single and multi-channel operations

## Hardware Requirements
- Raspberry Pi 4
- KK Flight Controller
- Camera Module
- Ultrasonic Sensor (for height measurement)
- Electromagnetic Gripper
- RC Receiver (Supported: Multi-channel and Single-channel configurations)
- Drone Frame and Motors
- Power Distribution System

## Software Architecture

### 1. RC Signal Processing Tools

#### Single Channel Receiver Testing (`Receiver_Single_Channel.py`)
- Standalone tool for testing and calibrating individual RC channels
- Features:
  - Real-time PWM signal monitoring
  - Precise pulse duration measurement
  - Edge detection capabilities
  - Signal validation
```python
def callback_function(GPIO_PIN, level, tick):
    if level == 1:  # rising edge
        start_time = tick
    elif level == 0:  # falling edge
        pulse_duration = pigpio.tickDiff(start_time, tick)
        # Process PWM signal
```

#### Multi-Channel Receiver Integration (`Receiver_Multi_Channel.py`)
- Complete receiver signal processing system
- Features:
  - Simultaneous multi-channel monitoring
  - Signal validation and filtering
  - Automatic failsafe detection
  - Servo control output


### 2. Altitude Control System (`Altitude_Hold.py`)
- Implements PID-based altitude control
- Features:
  - Height measurement using ultrasonic sensor
  - Hover throttle management
  - Signal loss detection
  - Emergency landing procedures
- Key Parameters:
  ```python
  hover_throttle = 1350
  max_throttle = 1700
  min_throttle = 1170
  target_altitude = 50  # cm
  ```
### 3. ArUco Marker Detection (`Aruco_Detect.py`)
- Real-time marker detection and position tracking
- Features:
  - Frame center calculation
  - Distance measurement
  - Direction determination (forward/backward/left/right)
  - Visual feedback system
- Supports both ArUco and color-based detection modes

### 4. Flight Control Interface (`Full_Function.py`)
- Main control logic integration
- Features:
  - Takeoff and landing procedures
  - Height maintenance
  - Signal monitoring
  - Emergency protocols
- Integrates various subsystems for coordinated operation

## Development Tools

### RC Signal Testing Tools
The project includes specialized tools for RC signal testing and validation:

1. **Single Channel Tester**
```python
# Initialize GPIO for single channel
pi.set_mode(GPIO_PIN, pigpio.INPUT)
pi.set_pull_up_down(GPIO_PIN, pigpio.PUD_DOWN)

# Callback for precise timing
def callback_function(GPIO_PIN, level, tick):
    if level == 1:  # rising edge
        start_time = tick
    elif level == 0:  # falling edge
        pulse_duration = pigpio.tickDiff(start_time, tick)
        print(f"PWM pulse duration: {pulse_duration} us")
```

2. **Multi-Channel Signal Processor**
```python
# Initialize multiple GPIO pins
GPIO_PINS = [17, 27, 22, 23, 24, 25]
pulse_durations = {pin: 0 for pin in GPIO_PINS}

# Process multiple channels
def servo_spin(pwm_signals):
    pwm_values = list(pwm_signals.values())
    if valid_signal_range(pwm_values):
        return pwm_values
```

## Setup and Installation

1. Install required Python packages:
```bash
pip install pigpio
pip install opencv-python
pip install numpy
pip install RPi.GPIO
```

2. Enable required interfaces:
```bash
sudo raspi-config
# Navigate to Interfacing Options
# Enable I2C, Camera, and GPIO
```

3. Start pigpio daemon:
```bash
sudo pigpiod
```

4. Test RC receiver setup:
```bash
# For single channel testing
python Receiver_Single_Channel.py

# For multi-channel testing
python Receiver_Multi_Channel.py
```

## Usage

1. Connect all hardware components according to the pinout configuration
2. Run the main control script:
```bash
python Full_Function.py
```

## Debugging and Testing

### RC Signal Debugging
1. Single Channel Testing:
   - Connect receiver channel to specified GPIO pin
   - Run single channel test script
   - Verify PWM signal timing (typical range: 1000-2000μs)
   - Check for signal stability and noise

2. Multi-Channel Validation:
   - Connect all channels to respective GPIO pins
   - Run multi-channel test script
   - Verify all channels respond correctly
   - Check for interference between channels

## Applications
- Warehouse Automation
- Inventory Management
- Automated Package Delivery
- Industrial Inspection
- Logistics Optimization

## Safety Features
- Signal loss detection
- Automatic landing on signal loss
- Throttle override capability
- Height limit enforcement
- Visual feedback system

## Future Improvements
1. Implement path planning algorithms
2. Add obstacle avoidance capabilities
3. Enhance package detection accuracy
4. Implement multiple drone coordination
5. Add battery monitoring system

## Contributing
Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.
## License
[MIT License](LICENSE)
## Contact
Karthickeien E

---
**Note**: This project is designed for research and development purposes. Always follow local regulations regarding drone operations.
