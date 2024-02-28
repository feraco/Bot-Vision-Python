import socket
import json
import time

class ArduinoCarController:
    def __init__(self, ip="192.168.4.1", port=100):
        self.ip = ip
        self.port = port

    def _connect(self):
        """Establishes connection to the car."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.port))
        print(f"Connected to {self.ip} on port {self.port}")

    def _disconnect(self):
        """Closes the socket connection."""
        if self.sock:
            self.sock.close()
            self.sock = None
            print("Disconnected")

    def _send_command(self, command):
        """Sends a JSON-encoded command to the car."""
        if not hasattr(self, 'sock') or self.sock is None:
            self._connect()
        json_command = json.dumps(command)
        print(f"Sending command: {json_command}")
        self.sock.sendall(json_command.encode())
        # Wait a bit for the command to be processed by the car
        time.sleep(0.5)

    def move_forward(self, duration_ms, speed):
        self._send_command({
            "N": 2,
            "D1": 1,  # Direction Forward
            "D2": speed,
            "T": duration_ms
        })
        time.sleep(duration_ms / 1000)

    def move_backward(self, duration_ms, speed):
        self._send_command({
            "N": 2,
            "D1": 2,  # Direction Backward
            "D2": speed,
            "T": duration_ms
        })
        time.sleep(duration_ms / 1000)

    def turn_left(self, duration_ms, speed):
        self._send_command({
            "N": 2,
            "D1": 3,  # Direction Left
            "D2": speed,
            "T": duration_ms
        })
        time.sleep(duration_ms / 1000)

    def turn_right(self, duration_ms, speed):
        self._send_command({
            "N": 2,
            "D1": 4,  # Direction Right
            "D2": speed,
            "T": duration_ms
        })
        time.sleep(duration_ms / 1000)

    def lighting_control_timed(self, sequence, red, green, blue, duration_ms):
        self._send_command({
            "N": 7,
            "D1": sequence,
            "D2": red,
            "D3": green,
            "D4": blue,
            "T": duration_ms
        })

    def lighting_control(self, sequence, red, green, blue):
        self._send_command({
            "N": 8,
            "D1": sequence,
            "D2": red,
            "D3": green,
            "D4": blue
        })

    def ultrasonic_sensor(self, status):
        self._send_command({
            "N": 21,
            "D1": status
        })

    def ir_sensor_line_tracking(self, status):
        self._send_command({
            "N": 22,
            "D1": status
        })

    def check_car_leaves_ground(self):
        self._send_command({
            "N": 23
        })

    def enter_standby_mode(self):
        self._send_command({
            "N": 100
        })

    def switch_car_mode(self, mode):
        self._send_command({
            "N": 101,
            "D1": mode
        })
    def set_motor_rotation(self, motor, speed, direction):
        """
        Sets individual motor rotation direction and speed.

        Parameters:
        - motor: Integer, selects the motor (1-4) to control.
        - speed: Integer (0-255), defines the speed of the motor.
        - direction: Integer (0 or 1), sets the rotation direction (0 for clockwise, 1 for counterclockwise).
        """
        self._send_command({
            "N": 1,
            "D1": motor,
            "D2": speed,
            "D3": direction
        })

    def set_servo_angle(self, servo, angle):
        """
        Sets the servo motor to a specific rotation angle.

        Parameters:
        - servo: Integer, selects the servo (1 for camera servo, 2 for ultrasonic sensor servo).
        - angle: Integer (0-180), the desired angle to set the servo to.
        """
        self._send_command({
            "N": 5,
            "D1": servo,
            "D2": angle
        })

    def joystick_move(self, direction, speed):
        """
        Moves the car in a specific direction with a given speed using joystick commands.

        Parameters:
        - direction: Integer (1-8), defines the direction to move (forward, backward, left, right, and diagonals).
        - speed: Integer (0-255), defines the speed of the movement.
        """
        self._send_command({
            "N": 102,
            "D1": direction,
            "D2": speed
        })

    def adjust_tracking_threshold(self, threshold):
        """
        Adjusts the tracking sensitivity of the car.

        Parameters:
        - threshold: Integer (0-255), adjusts the sensitivity threshold for line tracking.
        """
        self._send_command({
            "N": 104,
            "D1": threshold
        })
    def get_ultrasonic_distance(self):
        """Requests the distance measured by the ultrasonic sensor."""
        self._send_command({"N": 21})
        # Assuming the car immediately sends back a response with the distance
        data = self.sock.recv(1024).decode()
        distance_info = json.loads(data)
        return distance_info.get('distance', 0)

    def obstacle_avoidance(self):
        """Moves the car forward until an obstacle is detected, then turns."""
        try:
            while True:
                distance = self.get_ultrasonic_distance()
                if distance > 30:  # Safe distance threshold in cm
                    self.move_forward(1000, 200)  # Move forward with speed 200 for 1 second
                else:
                    self.turn_left(500, 200)  # Turn left with speed 200 for 0.5 second
                    # Additional logic to ensure it doesn't detect the same obstacle after turning
        except KeyboardInterrupt:
            print("Obstacle avoidance stopped.")
        finally:
            self._disconnect()
    def rotate_camera(self, direction):
        """
        Sets the camera rotation direction.

        Parameters:
        - direction: Integer, defines the camera rotation direction (1 for left, 2 for right).
        """
        self._send_command({
            "N": 106,
            "D1": direction
        })
    # Ensure the connection is closed if the controller is deleted
    def __del__(self):
        self._disconnect()

# Example usage
if __name__ == "__main__":
    car_controller = ArduinoCarController()
    # Move forward for 2 seconds at speed 150
    car_controller.move_forward(2000, 150)
    # Turn left for 1 second at speed 100
    car_controller.turn_left(1000, 100)
    # Additional commands can be added following the same pattern
