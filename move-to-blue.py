import cv2
import numpy as np
import socket
import json
import time
import requests

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

def detect_color(img, lower_color, upper_color):
    """Detect a specific color in the image."""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_color, upper_color)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

# Define the lower and upper bounds of the blue color in HSV
lower_blue = np.array([100, 150, 0])
upper_blue = np.array([140, 255, 255])

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
                contours = detect_color(img, lower_blue, upper_blue)
                
                # If blue color is detected
                if contours:
                    # Find the largest contour and its center
                    c = max(contours, key=cv2.contourArea)
                    M = cv2.moments(c)
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])
                        cv2.circle(img, (cx, cy), 5, (255, 0, 0), -1)
                        
                        # Decision for robot movement based on the color position
                        if cx < img.shape[1] // 3:
                            print("Turning Left")
                            send_command({"N": 2, "D1": 3, "D2": 200, "T": 1000})
                        elif cx > 2 * img.shape[1] // 3:
                            print("Turning Right")
                            send_command({"N": 2, "D1": 4, "D2": 200, "T": 1000})
                        else:
                            print("Moving Forward")
                            send_command({"N": 2, "D1": 1, "D2": 200, "T": 1000"})
                else:
                    print("No significant color detected, stopping.")
                    send_command({"N": 2, "D1": 0, "D2": 0, "T": 1000})  # Stop command

                cv2.imshow('Elegoo Smart Car Camera Stream', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            a = bytes_data.find(b'\xff\xd8')
            b = bytes_data.find(b'\xff\xd9')

cv2.destroyAllWindows()
