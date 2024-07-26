from danila.Danila_detail_CNN import Danila_detail_CNN


class Danila_detail():
    def __init__(self, danila_detail_params):
        self.danila_detail_params = danila_detail_params
        if (danila_detail_params.model_version == 1):
            self.danila_detail = Danila_detail_CNN(danila_detail_params.CNN_model_version)



    def detail_classify(self, img):
        return self.danila_detail.detail_classify(img)

