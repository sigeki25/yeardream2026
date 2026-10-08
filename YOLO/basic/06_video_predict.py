from ultralytics import YOLO

model = YOLO("yolo26n.pt")

results = model.predict(
    source="data/sample.mp4",  # 0 같은 숫자로 카메라로 지정 가능
    conf=0.5,
    show=True,  # 별도의 창으로 화면 보여주기
    save=False,  # 탐지내용 저장 여부
    imgsz=[480,640],
    exist_ok=True,
    verbose=False,  # 프레임관련 로그 출력 여부
    stream=True,  # 프레임 단위로 받아오기
    classes=[0],  # 인식할 클래스 지정(0 : 사람)
)

for r in results:
    boxes = r.boxes
    print(f"탐지 정보 : {boxes}")