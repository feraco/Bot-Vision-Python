import socket
import json
import time

# Set the IP and port for the car
ip = "192.168.4.1"
port = 100

# Define the command to move the car forward for 5 seconds at speed 150
command = {
    "N": 2,  # Car control mode with time limit
    "D1": 3,  # Direction (1 for forward, 2 for backward, adjust as needed)
    "D2": 150,  # Speed (0-255)
    "T": 5000  # Time in milliseconds
}

# Convert the command to a JSON string
json_command = json.dumps(command)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (ip, port)
print(f"Connecting to {ip} port {port}")
sock.connect(server_address)

try:
    # Send data
    print(f"Sending command: {json_command}")
    sock.sendall(json_command.encode())

    # Wait for the command to complete
    time.sleep(command["T"] / 1000)

finally:
    print("Closing socket")
    sock.close()

