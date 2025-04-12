import cv2
import numpy as np
from flask import Flask, jsonify, request
from ultralytics import YOLO

app = Flask(__name__)
model = YOLO("yolo11n-pose.pt")


@app.route("/pose", methods=["POST"])
def pose():
    file = request.files["image"]
    img_array = np.frombuffer(file.read(), np.uint8)
    frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    h, w = frame.shape

    results = model.predict(source=frame, task="pose", device="cpu", verbose=False)
    poses = results[0].keypoints.xy.tolist()  # send keypoints as list of coordinates
    pose = poses[0]
    nose = pose[0]
    nose[0] = (nose[0] - w / 2) / (w / 2)
    nose[1] = (nose[1] - h / 2) / (h / 2)

    return jsonify({"person": nose})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
