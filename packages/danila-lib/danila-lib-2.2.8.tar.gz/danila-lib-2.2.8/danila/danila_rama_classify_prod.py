from data.neuro.Rama_prod_classify_class import Rama_prod_classify_class
from data.neuro.models import RAMA_PROD_CLASSIFY_MODEL_ADDRESS, RAMA_PROD_CLASSIFY_MODEL_ADDRESS_2


class Danila_rama_classify_prod:
    def __init__(self, yolov5_dir, rama_classify_model):
        yolo_path = yolov5_dir
        if rama_classify_model == 1:
            rama_prod_classify_model_path = RAMA_PROD_CLASSIFY_MODEL_ADDRESS
        else:
            rama_prod_classify_model_path = RAMA_PROD_CLASSIFY_MODEL_ADDRESS_2
        print('reading and loading - RAMA_PROD_CLASSIFY_MODEL')
        self.rama_prod_classify_model = Rama_prod_classify_class(rama_prod_classify_model_path, yolo_path)

    def rama_classify(self, img):
        rama_prod_conf = self.rama_prod_classify_model.classify(img)
        return rama_prod_conf