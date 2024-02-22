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

# Load Tiny YOLO model
model_path = 'utils/resources/yolov3-tiny.weights'
config_path = 'utils/resources/yolov3-tiny.cfg'
net = cv2.dnn.readNet(model_path, config_path)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# Function to send commands to the Elegoo Smart Car
def send_command(command, IP="192.168.4.1", PORT=100):
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
    confidenceThreshold = 0.3
    nmsThreshold = 0.4
    try:
        while True:
            chunk = response.raw.read(1024)
            if not chunk:
                break
            bytes_data += chunk
            a = bytes_data.find(b'\xff\xd8')
            b = bytes_data.find(b'\xff\xd9')
            while a != -1 and b != -1:
                jpg = bytes_data[a:b+2]
                bytes_data = bytes_data[b+2:]
                if jpg:
                    img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    if img is not None and img.size > 0:
                        blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
                        net.setInput(blob)
                        layerNames = net.getLayerNames()
                        output_layer_indexes = net.getUnconnectedOutLayers().flatten()  # Ensure it's a flat array
                        outputNames = [layerNames[i - 1] for i in output_layer_indexes]
                        outputs = net.forward(outputNames)
                        
                        # Process detections
                        for output in outputs:
                            for detection in output:
                                scores = detection[5:]
                                classID = np.argmax(scores)
                                confidence = scores[classID]
                                if confidence > confidenceThreshold:
                                    center_x = int(detection[0] * img.shape[1])
                                    center_y = int(detection[1] * img.shape[0])
                                    width = int(detection[2] * img.shape[1])
                                    height = int(detection[3] * img.shape[0])
                                    
                                    x = int(center_x - width / 2)
                                    y = int(center_y - height / 2)
                                    
                                    cv2.rectangle(img, (x, y), (x + width, y + height), (0, 255, 0), 2)
                                    cv2.putText(img, f'{classNames[classID]} {int(confidence * 100)}%',
                                                (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                        
                        cv2.imshow('Elegoo Smart Car Camera Stream', img)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                    else:
                        print("Received an invalid image frame.")
                a = bytes_data.find(b'\xff\xd8')
                b = bytes_data.find(b'\xff\xd9')
    finally:
        cv2.destroyAllWindows()
else:
    print("Failed to connect to the camera stream.")
