import cv2
import math
import socket
import json
import time
from utils.PoseDetectorModule import PoseDetector

# Initialize the pose detector
detector = PoseDetector(upBody=True)

# Video capture
cap = cv2.VideoCapture(0)

# Elegoo Smart Car's IP and Port
IP = "192.168.4.1"
PORT = 100

def send_command(command):
    """Send a command to the Elegoo Smart Car."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((IP, PORT))
        sock.sendall(json.dumps(command).encode())
        time.sleep(0.5)  # Adjust based on your car's responsiveness

def calAngle(lmList, p1, p2, p3, draw=True, img=None):
    """Calculate the angle between three points."""
    if len(lmList) != 0 and img is not None:
        x1, y1 = lmList[p1][1:]
        x2, y2 = lmList[p2][1:]
        x3, y3 = lmList[p3][1:]
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
            cv2.line(img, (x2, y2), (x3, y3), (255, 0, 255), 2)
            cv2.circle(img, (x1, y1), 5, (255, 255, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 5, (255, 255, 0), cv2.FILLED)
            cv2.circle(img, (x3, y3), 5, (255, 255, 0), cv2.FILLED)
            cv2.putText(img, str(int(angle)), (x2 - 20, y2 - 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return angle
    return 0

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    img = detector.findPose(img, draw=True)
    lmList, bboxInfo = detector.findPosition(img, draw=True)

    if len(lmList) != 0:
        # Determine body poses and send corresponding commands
        angleR = calAngle(lmList, 12, 14, 16, draw=True, img=img)
        angleL = calAngle(lmList, 11, 13, 15, draw=True, img=img)

        # T-Pose: Move Forward
        if 160 < angleR < 180 and 160 < angleL < 180:
            cv2.putText(img, 'Moving Forward', (50, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            send_command({"N": 2, "D1": 1, "D2": 20, "T": 1000})

        # Arms Up: Stop (Just an example, modify as needed)
        elif angleR > 170 and angleL > 170:
            cv2.putText(img, 'Stop', (50, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            send_command({"N": 3, "D1": 0, "D2": 0})

        # Crossed Arms: Move Backward (Modify the condition based on your pose detection logic)
        # This part needs custom implementation based on how you detect crossed arms

    cv2.imshow('Elegoo Smart Car Control', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

