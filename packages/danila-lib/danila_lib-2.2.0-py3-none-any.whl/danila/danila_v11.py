from danila.danila_detail import Danila_detail
from data.result.Text_cut_recognize_result import Text_cut_recognize_result
from data.result.Text_recognize_result import Text_recognize_result


class Danila_v11:
    def __init__(self, yolov5_dir, detail_classify_version = 1,
                 rama_detect_version = 1, rama_classify_version = 1, rama_text_detect_version = 1, rama_text_recognize_version = 1,
                 vagon_text_detect_version = 1, vagon_text_recognize_version = 1,
                 balka_detect_version = 1, balka_classify_version = 1, balka_text_detect_version = 1, balka_text_recognize_version = 1):

        self.danila_detail = Danila_detail(Danila_detail_params(1,2))

    def detail_classify(self, img):
        return self.danila_detail.detail_classify(img)

    def detail_text_detect(self, img):
        return img

    def detail_text_recognize(self, img):
        return self.danila_detail.detail_classify(img)

    def rama_classify(self, img, detail = None):
        """rama_classify(Img : openCv frame): String - returns class of rama using CNN network"""
        """rama_classify uses Rama_classify_class method - classify(Img)"""
        detail_prod = Text_cut_recognize_result('rama', 1)
        det = Text_recognize_result(detail_prod)
        return det

    # returns openCV cut rama with drawn text areas
    def rama_text_detect_cut(self, img, detail = None):
        """returns openCV cut rama with drawn text areas"""
        return img


    # returns dict {'number', 'prod', 'year'} for openCV rama img or 'no_rama'
    def rama_text_recognize(self, img):
        """returns dict {'number', 'prod', 'year'} for openCV rama img or 'no_rama'"""
        return self.rama_classify(img)

    # returns openCV img with drawn number areas
    def vagon_number_detect(self, img):
        """returns openCV img with drawn number areas"""
        return img

    def vagon_number_recognize(self, img):
        return Text_recognize_result(Text_cut_recognize_result('vagon',1.0))


    def balka_classify(self, img):
        detail_prod = Text_cut_recognize_result('balka', 1)
        det = Text_recognize_result(detail_prod)
        return det

    def balka_text_detect(self, img):
        return img

    def balka_text_recognize(self, img):
        return self.balka_classify(img)