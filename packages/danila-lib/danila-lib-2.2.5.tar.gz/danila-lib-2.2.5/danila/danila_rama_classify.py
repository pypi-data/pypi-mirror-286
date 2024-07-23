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

    def rama_classify(self, img, detail):
        rama_prod_conf = self.danila_rama_classify.rama_classify(img)
        if detail is None:
            detail_prod = Text_cut_recognize_result('rama', 1)
            det = Text_recognize_result(detail_prod)
        else:
            det = detail
        if rama_prod_conf.rama_prod != Rama_Prod.no_rama:
            text_prod = PRODS[rama_prod_conf.rama_prod]
            det.prod = Text_cut_recognize_result(text_prod, rama_prod_conf.conf)
        return det
