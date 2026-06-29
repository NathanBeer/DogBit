import cv2
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
# Use a default index if the URL is unreachable
cap = cv2.VideoCapture("http://172.16.10.16:8080/video")

def look_for_object(target_name):
    if not cap.isOpened():
        print("[Seeing] Camera not connected!")
        return False
    
    ret, frame = cap.read()
    if not ret: return False
    
    results = model(frame, verbose=False)
    for result in results:
        for box in result.boxes:
            name = model.names[int(box.cls[0])]
            if target_name.lower() in name.lower():
                return True
    return False