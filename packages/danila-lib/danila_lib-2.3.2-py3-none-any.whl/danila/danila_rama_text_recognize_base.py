from data.neuro.models import TEXT_RECOGNIZE_RUZHIMMASH_MODEL_ADDRESS
from data.neuro.text_recognize_yolo import Text_Recognize_yolo
from data.result import Rama_prod
from data.result.Class_text import Class_text
from data.result.Rect import Rect


class Prod_coefficients:
    def __init__(self, number_coefficients, prod_coefficients, year_coefficients):
        self.number_coefficients = number_coefficients
        self.prod_coefficients = prod_coefficients
        self.year_coefficients = year_coefficients

class Text_coefficients:
    def __init__(self, length, height, width):
        self.length = length
        self.height = height
        self.width = width

class Danila_rama_text_recognize_base:
    def __init__(self, yolov5_dir, rama_text_recognize_version):

        if rama_text_recognize_version == 1:
            self.prod_coefficients = {
                Rama_prod.Rama_Prod.altai: Prod_coefficients(Text_coefficients(5, 64, 192),
                                                             Text_coefficients(4, 64, 128),
                                                             Text_coefficients(2, 64, 96)),
                Rama_prod.Rama_Prod.balakovo: Prod_coefficients(Text_coefficients(5, 64, 192),
                                                                Text_coefficients(4, 64, 192),
                                                                Text_coefficients(2, 64, 96)),
                Rama_prod.Rama_Prod.begickaya: Prod_coefficients(Text_coefficients(6, 96, 224),
                                                                 Text_coefficients(2, 64, 128),
                                                                 Text_coefficients(2, 64, 96)),
                Rama_prod.Rama_Prod.promlit: Prod_coefficients(Text_coefficients(5, 64, 160),
                                                               Text_coefficients(2, 64, 96),
                                                               Text_coefficients(2, 64, 96)),
                Rama_prod.Rama_Prod.ruzhimmash: Prod_coefficients(Text_coefficients(5, 64, 160),
                                                                  Text_coefficients(4, 64, 192),
                                                                  Text_coefficients(2, 64, 96)),
                Rama_prod.Rama_Prod.tihvin: Prod_coefficients(Text_coefficients(5, 64, 160),
                                                              Text_coefficients(4, 64, 224),
                                                              Text_coefficients(2, 64, 96)),
                Rama_prod.Rama_Prod.uralvagon: Prod_coefficients(Text_coefficients(5, 64, 192),
                                                                 Text_coefficients(1, 64, 64),
                                                                 Text_coefficients(2, 64, 96)),
            }
            print('reading and loading - RAMA_TEXT_RECOGNIZE_MODEL')
            self.text_recognize_model = Text_Recognize_yolo(TEXT_RECOGNIZE_RUZHIMMASH_MODEL_ADDRESS, yolov5_dir)

    def rama_text_recognize(self, rama_prod, img_cut, image_text_areas):
        label_area = self.text_recognize_model.work_image_cut(
            image_text_areas, img_cut,
            self.prod_coefficients[rama_prod].number_coefficients.length,
            self.prod_coefficients[rama_prod].number_coefficients.height,
            self.prod_coefficients[rama_prod].number_coefficients.width,
            self.prod_coefficients[rama_prod].prod_coefficients.length,
            self.prod_coefficients[rama_prod].prod_coefficients.height,
            self.prod_coefficients[rama_prod].prod_coefficients.width,
            self.prod_coefficients[rama_prod].year_coefficients.length,
            self.prod_coefficients[rama_prod].year_coefficients.height,
            self.prod_coefficients[rama_prod].year_coefficients.width
        )
        res_labels = {}
        (number_text, number_conf) = label_area.labels[Class_text.number]
        if len(number_text) == self.prod_coefficients[rama_prod].number_coefficients.length:
            res_labels['number'] = (number_text, number_conf)
        else:
            number_image_text_areas = image_text_areas.areas[Class_text.number]
            image_text_areas_min = []
            image_text_areas_max = []
            for number_image_text_area in number_image_text_areas:
                w = number_image_text_area.xmax - number_image_text_area.xmin
                if (number_image_text_area.xmin - (w // 2)) < 0:
                    new_xmin = 0
                else:
                    new_xmin = number_image_text_area.xmin - (w // 2)
                rect_min = Rect(xmin=new_xmin, xmax=number_image_text_area.xmax, ymin=number_image_text_area.ymin,
                                ymax=number_image_text_area.ymax)
                image_text_areas_min.append(rect_min)
                new_xmax = number_image_text_area.xmax + w // 2
                rect_max = Rect(xmin=number_image_text_area.xmin, xmax=new_xmax, ymin=number_image_text_area.ymin,
                                ymax=number_image_text_area.ymax)
                image_text_areas_max.append(rect_max)
            image_text_areas.areas[Class_text.number] = image_text_areas_min
            label_area_min = self.text_recognize_model.work_image_cut(
                image_text_areas, img_cut,
                self.prod_coefficients[rama_prod].number_coefficients.length,
                self.prod_coefficients[rama_prod].number_coefficients.height,
                self.prod_coefficients[rama_prod].number_coefficients.width,
                self.prod_coefficients[rama_prod].prod_coefficients.length,
                self.prod_coefficients[rama_prod].prod_coefficients.height,
                self.prod_coefficients[rama_prod].prod_coefficients.width,
                self.prod_coefficients[rama_prod].year_coefficients.length,
                self.prod_coefficients[rama_prod].year_coefficients.height,
                self.prod_coefficients[rama_prod].year_coefficients.width
            )
            (number_text_min, number_conf_min) = label_area_min.labels[Class_text.number]
            if len(number_text_min) == self.prod_coefficients[rama_prod].number_coefficients.length:
                res_labels['number'] = (number_text_min, number_conf_min)
            else:
                image_text_areas.areas[Class_text.number] = image_text_areas_max
                label_area_max = self.text_recognize_model.work_image_cut(
                    image_text_areas, img_cut,
                    self.prod_coefficients[rama_prod].number_coefficients.length,
                    self.prod_coefficients[rama_prod].number_coefficients.height,
                    self.prod_coefficients[rama_prod].number_coefficients.width,
                    self.prod_coefficients[rama_prod].prod_coefficients.length,
                    self.prod_coefficients[rama_prod].prod_coefficients.height,
                    self.prod_coefficients[rama_prod].prod_coefficients.width,
                    self.prod_coefficients[rama_prod].year_coefficients.length,
                    self.prod_coefficients[rama_prod].year_coefficients.height,
                    self.prod_coefficients[rama_prod].year_coefficients.width
                )
                (number_text_max, number_conf_max) = label_area_max.labels[Class_text.number]
                if len(number_text_max) == self.prod_coefficients[rama_prod].number_coefficients.length:
                    res_labels['number'] = (number_text_max, number_conf_max)
                else:
                    res_labels['number'] = (number_text, number_conf)
        (year_text, year_conf) = label_area.labels[Class_text.year]
        if (len(year_text) == 2) and (int(year_text) < 25):
            res_labels['year'] = (year_text, year_conf)
        else:
            res_labels['year'] = ('23', 0.25)
        return res_labels


