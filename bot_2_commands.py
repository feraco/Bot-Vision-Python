import socket
import json
import time

# Set the IP and port for the car
ip = "192.168.4.1"
port = 100

# Define multiple commands
commands = [
    {
        "N": 2,
        "D1": 3,
        "D2": 150,
        "T": 5000
    },
    {
        "N": 2,
        "D1": 1,
        "D2": 100,
        "T": 3000
    },
        {
        "N": 2,
        "D1": 2,
        "D2": 100,
        "T": 1000
    }
]

def send_command(command):
    # Convert the command to a JSON string
    json_command = json.dumps(command)
    
    # Create a new socket for each command
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect the socket to the server
        server_address = (ip, port)
        print(f"Connecting to {ip} port {port}")
        sock.connect(server_address)
        
        # Send data
        print(f"Sending command: {json_command}")
        sock.sendall(json_command.encode())
        
        # Wait for the command to complete before sending the next one
        time.sleep(command["T"] / 1000)

# Send each command in the list
for command in commands:
    try:
        send_command(command)
    except BrokenPipeError as e:
        print(f"Failed to send command: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
