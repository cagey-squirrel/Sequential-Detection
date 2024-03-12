from train import run


def main():

    data = 'yolov5s.yaml'
    run(imgsz=640, epochs=100, hyp='hyp.no-augmentation.yaml', data=data, weights='yolov5s.pt', cfg='models/yolov5s.yaml', patience=0)

if __name__ == "__main__":
    main()