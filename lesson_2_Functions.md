
# Python Lesson: Controlling an Arduino Smart Car

In this lesson, we will learn how to use the `ArduinoCarController` library to control a smart car by creating functions for specific movements. Before starting, make sure the `ArduinoCarController` class is correctly set up in your environment.

## Getting Started
First, import the `ArduinoCarController` from your library file.

```python
from arduino_car_controller import ArduinoCarController
```

Next, initialize your car controller object.

```python
car_controller = ArduinoCarController()
```

## Tasks
Below are the tasks you need to complete. For each task, create a function that performs the specified action. Use comments to explain each line of your code.

### 1. Turn Left 90 Degrees
- **Instructions**: Create a function named `turn_left_90` that makes the car turn left by 90 degrees.

### 2. Turn Right 90 Degrees
- **Instructions**: Create a function named `turn_right_90` that makes the car turn right by 90 degrees.

### 3. Turn 180 Degrees
- **Instructions**: Create a function named `turn_180` that makes the car turn 180 degrees, either left or right.

### 4. Move 1 Foot Forward
- **Instructions**: Create a function named `move_forward_1ft` that moves the car forward by 1 foot.

### 5. Move 2 Feet Forward
- **Instructions**: Create a function named `move_forward_2ft` that moves the car forward by 2 feet.

### 6. Move 3 Feet Forward
- **Instructions**: Create a function named `move_forward_3ft` that moves the car forward by 3 feet.

### 7. Move 1 Foot Backward
- **Instructions**: Create a function named `move_backward_1ft` that moves the car backward by 1 foot.

### 8. Move 2 Feet Backward
- **Instructions**: Create a function named `move_backward_2ft` that moves the car backward by 2 feet.

### 9. Move 3 Feet Backward
- **Instructions**: Create a function named `move_backward_3ft` that moves the car backward by 3 feet.

## Hints
- You may need to experiment with the duration and speed parameters to achieve the desired movements.
- Consider the relationship between speed, duration, and distance to calculate how long and at what speed the car should move to cover a specific distance.

## Submission
After completing the tasks, submit your Python script for review. Make sure your functions are well-commented to explain the logic behind your calculations and the choices you made for speed and duration.

Good luck, and have fun controlling your Arduino smart car!
