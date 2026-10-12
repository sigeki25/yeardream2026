from tabnanny import verbose

import cv2
from ultralytics import YOLO

model = YOLO("Computer Mouse.v2i.yolo26_best.pt")

cap = cv2.VideoCapture("data/mouse.mp4")

if not cap.isOpened():
    print("카메라 이상으로 시작할 수 없습니다.")
    exit()

while True:
    success, frame = cap.read()

    if not success:
        break

    # results = model.predict(
    #     frame,
    #     conf=0.1,
    #     imgsz=[480, 640],
    #     show=False,
    #     verbose=False,
    #     classes=[0]
    # )

    results = model.predict(
        frame,
        conf=0.5,
        imgsz=[480, 640],
        show=False,
        verbose=False,
        classes=[0, 1]
    )

    yolo_frame = results[0].plot()
    resize_frame = cv2.resize(yolo_frame, (480, 640))
    cv2.imshow("mouse_detect", resize_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()