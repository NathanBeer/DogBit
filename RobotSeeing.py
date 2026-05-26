from ultralytics import YOLO
import cv2

# Initialize model and camera once
model = YOLO("yolo26n.pt") 
cap = cv2.VideoCapture(0)

def look_for_object_single_frame(target_name):
    """Captures a frame, draws detections, and keeps the window stable."""
    ret, frame = cap.read()
    if not ret:
        return False

    results = model.predict(source=frame, conf=0.4, save=False, verbose=False)
    annotated_frame = results[0].plot()

    found = False
    for r in results:
        for box in r.boxes:
            label = model.names[int(box.cls[0])]
            if target_name in label.lower():
                found = True
    
    cv2.imshow("Robot Vision", annotated_frame)
    cv2.pollKey() 
    cv2.waitKey(1) 
    return found

def close_windows():
    """Hides the vision window and cleans up GUI events."""
    cv2.destroyAllWindows()
    # Briefly pulse waitKey to ensure Windows closes the actual window
    cv2.waitKey(1)