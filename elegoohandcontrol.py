import cv2
import numpy as np
import socket
import json
import time
import requests
from utils.HandTrackingModule import HandDetector

# Initialize the hand detector
detectorH = HandDetector(maxHands=2, detectionCon=0.8)

# Stream URL of the Elegoo Smart Car's camera
stream_url = "http://192.168.4.1:81/stream"

# Elegoo Smart Car's IP and Port
IP = "192.168.4.1"
PORT = 100

def send_command(command):
    """Send a command to the Elegoo Smart Car."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((IP, PORT))
        sock.sendall(json.dumps(command).encode())
        time.sleep(0.5)  # Adjust based on your car's responsiveness

# Start streaming session
session = requests.Session()
response = session.get(stream_url, stream=True)

if response.status_code == 200:
    bytes_data = bytes()
    while True:
        chunk = response.raw.read(1024)
        if not chunk:
            break
        bytes_data += chunk
        a = bytes_data.find(b'\xff\xd8')  # JPEG start
        b = bytes_data.find(b'\xff\xd9')  # JPEG end
        while a != -1 and b != -1:
            jpg = bytes_data[a:b+2]  # Extract JPEG
            bytes_data = bytes_data[b+2:]  # Remove processed bytes
            img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            
            if img is not None:
                img = detectorH.findHands(img)
                lmList, bbox = detectorH.findPosition(img, draw=True)
                if bbox:
                    fingers = detectorH.fingersUp()
                    # Define gestures for controlling the Elegoo Smart Car
                    if fingers == [1, 1, 1, 1, 1]:  # Open hand - Move Forward
                        send_command({"N": 2, "D1": 1, "D2": 200, "T": 1000})
                    elif fingers == [0, 1, 0, 0, 0]:  # Index finger - Move Backward
                        send_command({"N": 2, "D1": 2, "D2": 200, "T": 1000})
                    elif fingers == [0, 0, 0, 0, 1]:  # Pinky - Turn Left
                        send_command({"N": 2, "D1": 3, "D2": 200, "T": 1000})
                    elif fingers == [1, 0, 0, 0, 0]:  # Thumb - Turn Right
                        send_command({"N": 2, "D1": 4, "D2": 200, "T": 1000})
                    # Add more gestures as needed

                cv2.imshow('Elegoo Smart Car Camera Stream', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            a = bytes_data.find(b'\xff\xd8')
            b = bytes_data.find(b'\xff\xd9')

cv2.destroyAllWindows()
