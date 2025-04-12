import os

import cv2
from ultralytics import YOLO

# Force CPU before model is created
os.environ["CUDA_VISIBLE_DEVICES"] = ""
# Load YOLOv11 pose model
model = YOLO("yolo11n-pose.pt")  # Make sure the model path is correct

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to grab frame.")
        break

    # Run inference on CPU
    results = model.predict(
        source=frame,
        task="pose",
        conf=0.5,
        verbose=False,
        device="cpu",  # Force CPU usage
    )
    print(len(results[0].keypoints.xy.tolist()[0][0]))

    # Annotate and show
    annotated_frame = results[0].plot()
    cv2.imshow("YOLOv11 Pose Estimation (CPU)", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
