import os.path

import cv2

cap = cv2.VideoCapture("data/mouse.mp4")
save_dir = "dataset/source"

if not os.path.exists(save_dir):
    os.makedirs(save_dir)
    print("폴더 생성")

capture_cnt = 0
while True:
    success, frame = cap.read()


    if not success:
        break

    resize_frame = cv2.resize(frame, (480, 640))

    cv2.imshow("mouse", resize_frame)

    frame_cnt = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    if frame_cnt % 10 == 0:
        file_path = f"{save_dir}/{capture_cnt}.png"
        cv2.imwrite(file_path, resize_frame)
        capture_cnt += 1

    if cv2.waitKey(1) & 0xff == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()