import cv2
import numpy as np
import socket
import json
import time
import requests
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
                img = cv2.flip(img, 1)
                img = detector.findPose(img, draw=True)
                lmList, bboxInfo = detector.findPosition(img, draw=True)

                if len(lmList) != 0:
                    # Example poses
                    angleRightArmUp = detector.findAngle(img, 12, 14, 16, draw=True)
                    angleLeftArmUp = detector.findAngle(img, 11, 13, 15, draw=True)

                    # Moving Forward: Both arms raised
                    if angleRightArmUp < 30 and angleLeftArmUp < 30:
                        print("Moving Forward")
                        send_command({"N": 2, "D1": 1, "D2": 200, "T": 1000})

                    # Moving Backward: Both arms crossed
                    elif 140 < angleRightArmUp < 180 and 140 < angleLeftArmUp < 180:
                        print("Moving Backward")
                        send_command({"N": 2, "D1": 2, "D2": 200, "T": 1000})

                    # Turning Left: Left arm raised, right arm down
                    elif angleLeftArmUp < 30 and 140 < angleRightArmUp < 180:
                        print("Turning Left")
                        send_command({"N": 2, "D1": 3, "D2": 200, "T": 1000})

                    # Turning Right: Right arm raised, left arm down
                    elif angleRightArmUp < 30 and 140 < angleLeftArmUp < 180:
                        print("Turning Right")
                        send_command({"N": 2, "D1": 4, "D2": 200, "T": 1000})

                cv2.imshow('Elegoo Smart Car Camera Stream', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            a = bytes_data.find(b'\xff\xd8')
            b = bytes_data.find(b'\xff\xd9')

cv2.destroyAllWindows()
