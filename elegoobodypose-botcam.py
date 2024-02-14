import cv2
import math
import socket
import json
import time
import requests
import numpy as np
from utils.PoseDetectorModule import PoseDetector

# Initialize the pose detector
detector = PoseDetector(upBody=True)

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
    for chunk in response.iter_content(chunk_size=1024):
        bytes_data += chunk
        a = bytes_data.find(b'\xff\xd8')  # JPEG start
        b = bytes_data.find(b'\xff\xd9')  # JPEG end
        while a != -1 and b != -1:
            jpg = bytes_data[a:b+2]  # Extract JPEG
            bytes_data = bytes_data[b+2:]  # Remove processed bytes
            img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

            if img is not None:
                img = cv2.flip(img, 1)
                img = detector.findPose(img, draw=True)
                lmList, bboxInfo = detector.findPosition(img, draw=True)

                if len(lmList) != 0:
                    # Example: Detect specific poses and control the car
                    angleR = detector.findAngle(img, 12, 14, 16, draw=True)
                    angleL = detector.findAngle(img, 11, 13, 15, draw=True)

                    # Implement your conditions for pose detection and corresponding car commands
                    # Example: T-Pose detected
                    if 160 < angleR < 180 and 160 < angleL < 180:
                        cv2.putText(img, 'Moving Forward', (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                        send_command({"N": 2, "D1": 1, "D2": 200, "T": 1000})

                cv2.imshow('Elegoo Smart Car Camera Stream', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            a = bytes_data.find(b'\xff\xd8')
            b = bytes_data.find(b'\xff\xd9')

cv2.destroyAllWindows()
