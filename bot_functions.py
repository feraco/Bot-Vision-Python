import socket
import json
import time

# Global variables for the car's IP address and port
ip = "192.168.4.1"
port = 100

# Function to send commands to the car
def create_socket_and_send(json_command):
    """
    Creates a socket connection, sends a command to the car, and closes the connection.
    
    :param json_command: A JSON string representing the command to be sent to the car.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        print(f"Sending command: {json_command}")
        sock.sendall(json_command.encode())
        # Wait a bit for the command to be processed by the car
        time.sleep(0.5)

# Command function to move the car forward
def move_forward(duration_ms, speed):
    """
    Commands the car to move forward.
    
    :param duration_ms: The duration in milliseconds for which the car should move forward.
    :param speed: The speed at which the car should move (0-255).
    """
    command = {
        "N": 2,
        "D1": 1,  # Direction Left
        "D2": speed,
        "T": duration_ms
    }
    create_socket_and_send(json.dumps(command))
    time.sleep(duration_ms / 1000)

# Command function to move the car backward
def move_backward(duration_ms, speed):
    """
    Commands the car to move backward.
    
    :param duration_ms: The duration in milliseconds for which the car should move backward.
    :param speed: The speed at which the car should move (0-255).
    """
    command = {
        "N": 2,
        "D1": 2,  # Direction Right
        "D2": speed,
        "T": duration_ms
    }
    create_socket_and_send(json.dumps(command))
    time.sleep(duration_ms / 1000)

# Command function to turn the car left
def turn_left(duration_ms, speed):
    """
    Commands the car to turn left.
    
    :param duration_ms: The duration in milliseconds for which the car should turn left.
    :param speed: The speed at which the car should turn (0-255).
    """
    command = {
        "N": 2,
        "D1": 3,  # Direction Foward
        "D2": speed,
        "T": duration_ms
    }
    create_socket_and_send(json.dumps(command))
    time.sleep(duration_ms / 1000)

# Command function to turn the car right
def turn_right(duration_ms, speed):
    """
    Commands the car to turn right.
    
    :param duration_ms: The duration in milliseconds for which the car should turn right.
    :param speed: The speed at which the car should turn (0-255).
    """
    command = {
        "N": 2,
        "D1": 4,  # Direction Backward
        "D2": speed,
        "T": duration_ms
    }
    create_socket_and_send(json.dumps(command))
    time.sleep(duration_ms / 1000)
    
# Function to control lighting with a time limit
def lighting_control_timed(sequence, red, green, blue, duration_ms):
    """
    Controls the car's lighting in a specified sequence with RGB values for a limited time.
    
    :param sequence: Lighting sequence (e.g., left, front, right, back, center).
    :param red: Red color value (0-255).
    :param green: Green color value (0-255).
    :param blue: Blue color value (0-255).
    :param duration_ms: Duration in milliseconds for the lighting effect.
    """
    command = {
        "N": 7,
        "D1": sequence,
        "D2": red,
        "D3": green,
        "D4": blue,
        "T": duration_ms
    }
    create_socket_and_send(json.dumps(command))

# Function to control lighting without a time limit
def lighting_control(sequence, red, green, blue):
    """
    Controls the car's lighting in a specified sequence with RGB values without a time limit.
    
    :param sequence: Lighting sequence.
    :param red: Red color value (0-255).
    :param green: Green color value (0-255).
    :param blue: Blue color value (0-255).
    """
    command = {
        "N": 8,
        "D1": sequence,
        "D2": red,
        "D3": green,
        "D4": blue
    }
    create_socket_and_send(json.dumps(command))

# Function to control the ultrasonic sensor
def ultrasonic_sensor(status):
    """
    Controls the ultrasonic sensor's mode or status.
    
    :param status: Status or mode for the ultrasonic sensor (e.g., 1 for start detection).
    """
    command = {
        "N": 21,
        "D1": status
    }
    create_socket_and_send(json.dumps(command))

# Function for IR sensor in line tracking mode
def ir_sensor_line_tracking(status):
    """
    Sets the IR sensor to line tracking mode or checks its data.
    
    :param status: Status or mode for the IR sensor (e.g., 1 for line detection).
    """
    command = {
        "N": 22,
        "D1": status
    }
    create_socket_and_send(json.dumps(command))

# Function to check if the car leaves the ground
def check_car_leaves_ground():
    """
    Checks if the car has left the ground. No additional parameters required.
    """
    command = {
        "N": 23
    }
    create_socket_and_send(json.dumps(command))

# Function to enter standby mode
def enter_standby_mode():
    """
    Clears all functions and enters standby mode.
    """
    command = {
        "N": 100
    }
    create_socket_and_send(json.dumps(command))

# Function to switch car mode (e.g., remote control)
def switch_car_mode(mode):
    """
    Switches the car's mode, such as TraceBased, ObstacleAvoidance, or Follow.
    
    :param mode: Mode selection (e.g., 1 for TraceBased).
    """
    command = {
        "N": 101,
        "D1": mode
    }
    create_socket_and_send(json.dumps(command))


# Example usage
if __name__ == "__main__":
    # Move forward for 2 seconds at speed 150
    move_forward(2000, 150)
    # Turn left for 1 second at speed 100
    turn_left(1000, 100)
    # Move backward for 2 seconds at speed 150
    move_backward(2000, 150)
    # Turn right for 1 second at speed 100
    turn_right(1000, 100)
    lighting_control_timed(sequence=1, red=255, green=0, blue=0, duration_ms=5000)
    # Switch car mode to Obstacle Avoidance
    switch_car_mode(mode=2)
    # Enter standby mode after 10 seconds
    time.sleep(10)
    enter_standby_mode()
