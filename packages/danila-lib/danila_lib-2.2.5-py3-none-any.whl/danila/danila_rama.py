from danila.danila_rama_classify import Danila_rama_classify


class Danila_rama:
    def __init__(self, yolov5_dir, danila_rama_params):
        self.danila_rama_params = danila_rama_params
        self.danila_rama_classify = Danila_rama_classify(yolov5_dir, self.danila_rama_params.danila_rama_classify_params)

    def rama_classify(self,img,detail):
        self.danila_rama_classify.rama_classify(img,detail)