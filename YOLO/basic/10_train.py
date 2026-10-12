from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO("yolo26n.pt")
    # results = model.train(
    #     data="dataset/dataset/data.yaml",
    #     exist_ok=True,
    #     epochs=100,
    #     imgsz=[480, 640],
    #     batch=64,
    #     workers=4
    # )

    results = model.train(
        data="dataset/dataset2/data.yaml",
        exist_ok=True,
        epochs=10,
        imgsz=[480, 640],
        batch=16,
        workers=2
    )
    print("모델 학습 완료")
    print(f"종합 점수")
    print(results.results_dict)