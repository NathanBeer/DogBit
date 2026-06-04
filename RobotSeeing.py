import cv2
from ultralytics import YOLO

def get_model_classes():
    # If your model variable is named 'model', it should look like this:
    return model.names.values()

model = YOLO('yolov8n.pt')

def get_frame():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    return frame if ret else None

def look_for_object_single_frame(target_name):
    frame = get_frame()
    if frame is None: return False
    results = model(frame, verbose=False)
    for result in results:
        for box in result.boxes:
            if model.names[int(box.cls[0])].lower() == target_name.lower():
                return True
    return False