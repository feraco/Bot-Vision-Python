
# Elegoo Smart Car V4 Programming Course

Welcome to the Elegoo Smart Car V4 Programming Course repository, curated by Frederick Feraco. This course is designed to introduce students to the fascinating world of robotics and programming through hands-on experience with the Elegoo Smart Car V4. By using Python, one of the most versatile programming languages, students will learn how to control and extend the capabilities of the smart car, exploring concepts like object detection, face tracking, and gesture control.

## Objective

The primary goal of this course is to provide a comprehensive learning experience that combines theory with practical applications. Students will engage with a series of Jupyter Notebooks that progressively build their understanding and skills in robotics programming, computer vision, and network communication.

## Prerequisites
Instructions Summary:
Create a Virtual Environment:

Navigate to your project directory in the terminal.
Run 
```bash
python -m venv venv
```
or 
```bash
python3 -m venv venv
```
to create a virtual environment named venv.
Activate the Virtual Environment:

On Windows, run
```bash
 .\\venv\\Scripts\\activate.
   ```

On macOS and Linux, run  
```bash
source venv/bin/activate.  
```
Install Dependencies:

Ensure you have a requirements.txt file in the project directory.
Run 
```bash
pip install -r requirements.txt
```
to install the required packages.
Before you begin, ensure you have the following:
- **Python 3.x installed**: Make sure you have a Python 3.x environment set up. You can download Python from [python.org](https://www.python.org/downloads/).
- **OpenCV and other dependencies**: This course requires OpenCV, NumPy, and Requests libraries. You can install these using pip:
```bash
  pip install opencv-python-headless numpy requests
  ```
- **Elegoo Smart Car V4**: This course is designed specifically for the Elegoo Smart Car V4. Ensure your car is assembled and ready for programming.
- **Camera Setup**: A camera mounted on the Elegoo Smart Car, accessible through a stream URL.

## Course Content

The course is divided into several modules, each focusing on a different aspect of programming the Elegoo Smart Car V4:

1. **Introduction to Elegoo Smart Car Control**: Learn the basics of sending commands to control the car's movement.
2. **Object Detection Controlled Car**: Dive into computer vision with object detection to control car movements.
3. **Face Following Car**: Explore face detection techniques to make the car follow a person.
4. **Hand Gesture Controlled Car**: Implement hand gesture recognition to control the car's actions.

Each module is contained in its own Jupyter Notebook, providing a mix of instructional content, code examples, and exercises.

## Getting Started

To begin the course, clone this repository to your local machine:

```bash
git clone https://github.com/feraco/Bot-Vision-Python.git
```

Navigate to the repository directory and start Jupyter Notebook:

```bash
cd Bot-Vision-Python
jupyter notebook
```

Open the first notebook in the series and follow the instructions contained within.

## Contributing

We welcome contributions and suggestions! If you have ideas for improving the course or want to add more content, please feel free to fork the repository, make your changes, and submit a pull request.

## About the Developer

Frederick Feraco is a dedicated developer and educator passionate about bringing robotics and programming closer to students of all ages. With a background in computer science and extensive experience in teaching, Frederick aims to create engaging, educational content that inspires and equips the next generation of programmers and engineers.

# Detailed Reference Guide for ArduinoCarController Functions

## Class Overview
The `ArduinoCarController` class provides methods to control an Arduino-based smart car remotely. Below is a detailed guide on each method, explaining its purpose and usage.

### move_forward(duration_ms, speed)
- **Purpose**: Commands the car to move forward.
- **Parameters**:
  - `duration_ms`: The duration in milliseconds for which the car should move forward.
  - `speed`: The speed at which the car should move (0-255).
- **Usage**:
  ```python
  car_controller.move_forward(2000, 150)
  ```

### move_backward(duration_ms, speed)
- **Purpose**: Commands the car to move backward.
- **Parameters**:
  - `duration_ms`: The duration in milliseconds for which the car should move backward.
  - `speed`: The speed at which the car should move (0-255).
- **Usage**:
  ```python
  car_controller.move_backward(1000, 100)
  ```

### turn_left(duration_ms, speed)
- **Purpose**: Commands the car to turn left.
- **Parameters**:
  - `duration_ms`: The duration in milliseconds for which the car should turn left.
  - `speed`: The speed at which the car should turn (0-255).
- **Usage**:
  ```python
  car_controller.turn_left(500, 100)
  ```

### turn_right(duration_ms, speed)
- **Purpose**: Commands the car to turn right.
- **Parameters**:
  - `duration_ms`: The duration in milliseconds for which the car should turn right.
  - `speed`: The speed at which the car should turn (0-255).
- **Usage**:
  ```python
  car_controller.turn_right(500, 100)
  ```

### lighting_control_timed(sequence, red, green, blue, duration_ms)
- **Purpose**: Controls the car's lighting with specified RGB values for a limited time.
- **Parameters**:
  - `sequence`: Lighting sequence (e.g., left, front, right, back, center).
  - `red`: Red color value (0-255).
  - `green`: Green color value (0-255).
  - `blue`: Blue color value (0-255).
  - `duration_ms`: Duration in milliseconds for the lighting effect.
- **Usage**:
  ```python
  car_controller.lighting_control_timed(1, 255, 0, 0, 5000)
  ```

### lighting_control(sequence, red, green, blue)
- **Purpose**: Controls the car's lighting with specified RGB values without a time limit.
- **Parameters**:
  - `sequence`: Lighting sequence.
  - `red`: Red color value (0-255).
  - `green`: Green color value (0-255).
  - `blue`: Blue color value (0-255).
- **Usage**:
  ```python
  car_controller.lighting_control(1, 255, 255, 255)
  ```

### ultrasonic_sensor(status)
- **Purpose**: Controls the ultrasonic sensor's mode or status.
- **Parameters**:
  - `status`: Status or mode for the ultrasonic sensor (e.g., 1 for start detection).
- **Usage**:
  ```python
  car_controller.ultrasonic_sensor(1)
  ```

### ir_sensor_line_tracking(status)
- **Purpose**: Sets the IR sensor to line tracking mode or checks its status.
- **Parameters**:
  - `status`: Status or mode for the IR sensor (e.g., 1 for line detection).
- **Usage**:
  ```python
  car_controller.ir_sensor_line_tracking(1)
  ```

### check_car_leaves_ground()
- **Purpose**: Checks if the car has left the ground. No additional parameters required.
- **Usage**:
  ```python
  car_controller.check_car_leaves_ground()
  ```

### enter_standby_mode()
- **Purpose**: Clears all functions and enters standby mode.
- **Usage**:
  ```python
  car_controller.enter_standby_mode()
  ```

### switch_car_mode(mode)
- **Purpose**: Switches the car's mode, such as TraceBased, ObstacleAvoidance, or Follow.
- **Parameters**:
  - `mode`: Mode selection (e.g., 1 for TraceBased).
- **Usage**:
  ```python
  car_controller.switch_car_mode(1)
  ```

This guide aims to provide clear instructions on how to use each function within the ArduinoCarController class effectively.

