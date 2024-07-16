import cv2
from sort import *
import math
import numpy as np
from ultralytics import YOLO
import cvzone
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

cap = cv2.VideoCapture("test_Trim.mp4")


model = YOLO("runs/detect/train2/weights/best.pt").to(device)

classname = {0: "shrimp"}

trackers = Sort(max_age=20)

frame_width = 420
frame_height = 640

line = [320, 0, 320, 640]
counter = []

fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # codec for mp4 format
out = cv2.VideoWriter("output.mp4", fourcc, 20.0, (frame_width, frame_height))

while 1:
    ret, frame = cap.read()
    if not ret:
        cap = cv2.videocapture("test_Trim.mp4")
        continue
    frame = cv2.resize(frame, (frame_width, frame_height))

    detections = np.empty((0, 5), int)

    results = model(frame, stream=1)
    for info in results:
        boxes = info.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            conf = box.conf[0]
            classindex = box.cls[0]

            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            conf = math.ceil(conf * 100)
            classindex = int(classindex)
            new_detection = np.array([x1, y1, x2, y2, conf])
            detections = np.vstack((detections, new_detection))
            # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # cvzone.putTextRect(
            #     frame,
            #     f"{classname[classindex]}: {conf}%",
            #     ([x1 + 8, y1 - 12]),
            #     thickness=2,
            #     scale=1.5,
            # )
            # print(classindex)

    track_result = trackers.update(detections)
    cv2.line(frame, (line[0], line[1]), (line[2], line[3]), (0, 255, 255), 2)
    for results in track_result:
        x1, y1, x2, y2, track_id = results
        x1, y1, x2, y2, track_id = int(x1), int(y1), int(x2), int(y2), int(track_id)
        w, h = x2 - x1, y2 - y1
        cx, cy = x1 + w // 2, y1 + h // 2

        cv2.circle(frame, (cx, cy), 6, (0, 0, 255), -1)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # cvzone.putTextRect(
        #     frame,
        #     f"ID: {track_id}",
        #     ([x1 + 8, y1 - 12]),
        #     thickness=2,
        #     scale=1.5,
        # )
        if line[0] - 20 < cx < line[2] + 20 and line[1] < cy < line[3]:
            cv2.line(frame, (line[0], line[1]), (line[2], line[3]), (255, 0, 0), 2)
            if counter.count(track_id) == 0:
                counter.append(track_id)

    cvzone.putTextRect(
        frame,
        f"Counter: {len(counter)}",
        [10, 50],
        thickness=2,
        scale=2,
    )
    out.write(frame)
    cv2.imshow("frame", frame)
    cv2.waitKey(1)
