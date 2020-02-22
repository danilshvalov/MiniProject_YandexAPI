import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap, QFont
from PyQt5 import uic, QtCore
import requests


class Maps:
    def __init__(self):
        self.toponym_to_find = "Владивосток"
        self.delta = 0.01
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
            "spn": ','.join([str(self.delta), str(self.delta)]),
            "l": "map",
        }
        response_api = requests.get(map_api_server, params=map_params)
        if not response_api:
            raise Exception
        with open(self.maps, "wb") as file:
            file.write(response_api.content)
            file.close()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.maps_api = Maps()
        self.pixmap = QPixmap(self.maps_api.maps)
        self.label.setPixmap(self.pixmap)


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())