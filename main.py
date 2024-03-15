from train import run


def main():

    data = 'brain_tumor_detection.yaml'
    weights = 'yolov5s.pt'
    weights = '/media/workstation/Disk 1/sequential_detection/Sequential-Detection/runs/train/exp46/weights/best.pt'
    run(imgsz=640, epochs=1, hyp='hyp.no-augmentation.yaml', data=data, weights=weights, cfg='models/yolov5s.yaml', patience=0)
    #run(imgsz=640, epochs=100, data=data, weights='yolov5s.pt', cfg='models/yolov5s.yaml', patience=0)

if __name__ == "__main__":
    main()