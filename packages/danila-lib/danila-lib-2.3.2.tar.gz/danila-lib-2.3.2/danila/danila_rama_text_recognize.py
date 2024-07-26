from danila.danila_rama_text_recognize_base import Danila_rama_text_recognize_base


class Danila_rama_text_recognize:
    def __init__(self, yolov5_dir, danila_rama_text_recognize_params):
        self.danila_rama_text_recognize_params = danila_rama_text_recognize_params
        self.danila_rama_text_recognize = Danila_rama_text_recognize_base(yolov5_dir,
                                                                    self.danila_rama_text_recognize_params.rama_text_recognize_version
                                                                    )

    def rama_text_recognize(self, rama_prod, img_cut, img_text_areas):
        return self.danila_rama_text_recognize.rama_text_recognize(rama_prod, img_cut, img_text_areas)