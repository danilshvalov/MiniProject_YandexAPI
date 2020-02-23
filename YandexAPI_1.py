import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import uic, QtCore
from Maps import Maps


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.width_map, self.height_map = 650, 450
        self.setGeometry(100, 100, self.width_map, self.height_map + 120)
        self.maps_api = Maps()
        self.update_image()
        self.label.resize(650, 450)
        self.label.move(0, 0)
        self.button_map.setChecked(True)
        self.button_map.clicked.connect(self.change_mapstyle)
        self.button_sat.clicked.connect(self.change_mapstyle)
        self.button_sklsat.clicked.connect(self.change_mapstyle)
        self.button_find.clicked.connect(self.find_object)
        self.button_cancel.clicked.connect(self.cancel_find)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_PageUp:
            self.maps_api.map_moving("pg_up")
            self.update_image()
        elif e.key() == QtCore.Qt.Key_PageDown:
            self.maps_api.map_moving("pg_down")
            self.update_image()
        elif e.key() == QtCore.Qt.Key_W:
            self.maps_api.map_moving("up")
            self.update_image()
        elif e.key() == QtCore.Qt.Key_S:
            self.maps_api.map_moving("down")
            self.update_image()
        elif e.key() == QtCore.Qt.Key_D:
            self.maps_api.map_moving("right")
            self.update_image()
        elif e.key() == QtCore.Qt.Key_A:
            self.maps_api.map_moving("left")
            self.update_image()

    def update_image(self):
        map_image = QImage(self.maps_api.image_map(), self.width_map, self.height_map, QImage.Format_RGBX8888)
        self.label.setPixmap((QPixmap.fromImage(map_image)))

    def change_mapstyle(self):
        if self.button_map.isChecked() is True:
            self.maps_api.mapstyle = 'map'
        elif self.button_sat.isChecked() is True:
            self.maps_api.mapstyle = 'sat'
        elif self.button_sklsat.isChecked() is True:
            self.maps_api.mapstyle = 'sat,skl'
        self.update_image()

    def find_object(self):
        if self.find_text.text():
            self.maps_api.find_object(self.find_text.text())
            self.update_image()
        self.address.setText(self.maps_api.address)

    def cancel_find(self):
        self.maps_api.point = ''
        self.update_image()
        self.address.setText('')


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())