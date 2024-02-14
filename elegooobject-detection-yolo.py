import cv2
import numpy as np
import socket
import json
import time
import requests

# Load class names
classNames = []
with open('utils/resources/coco.names', 'r') as f:
    classNames = f.read().splitlines()

# Load YOLO model
model = 'utils/resources/yolov3.weights'
config = 'utils/resources/yolov3.cfg'
net = cv2.dnn.readNet(model, config)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# Elegoo Smart Car's IP and Port
IP = "192.168.4.1"
PORT = 100

# Function to send commands to the Elegoo Smart Car
def send_command(command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((IP, PORT))
        sock.sendall(json.dumps(command).encode())
        time.sleep(0.5)  # Adjust based on your car's responsiveness

# Stream URL of the Elegoo Smart Car's camera
stream_url = "http://192.168.4.1:81/stream"

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
                blob = cv2.dnn.blobFromImage(img, 1 / 255, (320, 320), (0, 0, 0), crop=False)
                net.setInput(blob)
                layerNames = net.getLayerNames()
                outputNames = [layerNames[i-1] for i in net.getUnconnectedOutLayers()]
                outputs = net.forward(outputNames)
                
                # Object Detection and Decision Logic Here
                # Example: findObject(outputs, img) and based on detection, send commands
                # Adapt `findObject` function to include command sending logic based on detected objects

                cv2.imshow('Elegoo Smart Car Camera Stream', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            a = bytes_data.find(b'\xff\xd8')
            b = bytes_data.find(b'\xff\xd9')

cv2.destroyAllWindows()
