import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap, QFont, QImage
from PyQt5 import uic, QtCore
import requests
from PIL import Image
from io import BytesIO


class Maps:
    def __init__(self):
        self.width_map, self.height_map = 650, 450
        self.toponym_to_find = "Владивосток"
        self.delta = 17
        self.find_coords()
        self.maps = "map.png"
        self.image_map()

    def find_coords(self):
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": self.toponym_to_find,
            "format": "json"}
        response_geo = requests.get(geocoder_api_server, params=geocoder_params)
        if not response_geo:
            raise Exception
        self.coords = ','.join(response_geo.json()["response"]["GeoObjectCollection"]
                               ["featureMember"][0]["GeoObject"]["Point"]["pos"].split())

    def image_map(self):
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        map_params = {
            "ll": self.coords,
            "z": str(self.delta),
            "l": "sat",
            'size': f'{self.width_map},{self.height_map}'
        }
        response_api = requests.get(map_api_server, params=map_params)
        if not response_api:
            raise Exception

        self.maps = Image.open(BytesIO(response_api.content)).convert('RGBX').tobytes()
        return self.maps


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.width_map, self.height_map = 650, 450
        self.setGeometry(100, 100, self.width_map, self.height_map)
        self.maps_api = Maps()
        map_image = QImage(self.maps_api.image_map(), self.width_map, self.height_map, QImage.Format_RGBX8888)
        self.label.setPixmap((QPixmap.fromImage(map_image)))
        self.label.resize(650, 450)
        self.label.move(0, 0)


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())