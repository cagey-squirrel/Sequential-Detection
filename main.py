from train import run


def main():

    data = 'brain_tumor_detection.yaml'
    weights = 'yolov5s.pt'
    cfgs = ['models/yolov5m.yaml']
    datas = ['data_yamls/brain_tumor_detection.yaml']
    weights = 'yolov5m.pt'
    for data in datas:
        for cfg in cfgs:
            if 'custom' in cfg:
                sequential = True
            else:
                sequential = False
            run(imgsz=256, epochs=100, hyp='hyp.no-augmentation.yaml', data=data, weights=weights, cfg=cfg, patience=0, sequential=sequential)


if __name__ == "__main__":
    main()