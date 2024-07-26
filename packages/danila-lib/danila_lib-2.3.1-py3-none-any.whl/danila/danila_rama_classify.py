from danila.danila_rama_classify_prod import Danila_rama_classify_prod
from data.neuro.prods import PRODS
from data.result.Rama_prod import Rama_Prod
from data.result.Text_cut_recognize_result import Text_cut_recognize_result
from data.result.Text_recognize_result import Text_recognize_result


class Danila_rama_classify:
    def __init__(self, yolov5_dir, danila_rama_classify_params):
        self.danila_rama_classify_params = danila_rama_classify_params
        if self.danila_rama_classify_params.rama_classify_version == 1:
            self.danila_rama_classify = Danila_rama_classify_prod(yolov5_dir, self.danila_rama_classify_params.rama_classify_model)

    def rama_classify(self, img):
        return self.danila_rama_classify.rama_classify(img)

