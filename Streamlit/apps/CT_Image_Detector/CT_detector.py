import torch
import torch.nn as nn

from apps.CT_Image_Detector.yolov5.detect import run

class Detector:
    def __init__(self,
                image="apps/CT_Image_Detector/images/049fce8128f9.jpg"):
        self.model_path="apps/CT_Image_Detector/model/best.pt"
        self.image_path=image
        self.img_size=256
        self.conf_thres=0.3
        self.iou_thres=0.5

    def predict_(self):
        run(weights=self.model_path,
            source=self.image_path,
            imgsz=self.img_size,
            conf_thres=self.conf_thres,
            iou_thres=self.iou_thres,
            max_det=1000,
            device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
            view_img=False,  # show results
            save_txt=True,  # save results to *.txt
            save_conf=True,  # save confidences in --save-txt labels
            save_crop=False,  # save cropped prediction boxes
            nosave=False,  # do not save images/videos
            classes=None,
            agnostic_nms=False,
            augment=False,
            visualize=False,
            update=False,
            project='apps/CT_Image_Detector/runs/prediction',  # save results to project/name
            name='exp',  # save results to project/name
            exist_ok=False,
            line_thickness=1,  # bounding box thickness (pixels)
            hide_labels=False,
            hide_conf=False,
            half=False,  # use FP16 half-precision inference)
        )
        return {
            'image':'apps/CT_Image_Detector/runs/prediction/exp/' + self.image_path.split('/')[-1],
            'label':'apps/CT_Image_Detector/runs/prediction/exp/labels/' + self.image_path.split('/')[-1].replace('jpg', 'txt')
        }

