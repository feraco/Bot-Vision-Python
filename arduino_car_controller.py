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
