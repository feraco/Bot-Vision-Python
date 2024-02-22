
from arduino_car_controller import ArduinoCarController
import time

# Initialize the controller
controller = ArduinoCarController()

# Ensure we connect to the car before sending commands
try:
    controller._connect()
    print("Successfully connected to the robot.")

    # Move forward
    print("Moving forward")
    controller.car_control_time_limit("forward", 255, 2000)  # Move forward for 2 seconds at speed 255
    time.sleep(2.5)  # Wait a bit longer than the action to ensure completion

    # Move backward
    print("Moving backward")
    controller.car_control_time_limit("backward", 255, 2000)  # Move backward for 2 seconds at speed 255
    time.sleep(2.5)  # Wait a bit longer than the action to ensure completion

    # Move left
    print("Turning left")
    controller.car_control_time_limit("left", 255, 2000)  # Turn left for 2 seconds at speed 255
    time.sleep(2.5)  # Wait a bit longer than the action to ensure completion

    # Move right
    print("Turning right")
    controller.car_control_time_limit("right", 255, 2000)  # Turn right for 2 seconds at speed 255
    time.sleep(2.5)  # Wait a bit longer than the action to ensure completion

finally:
    # Disconnect after all movements are done
    controller._disconnect()
    print("Disconnected from the robot.")
