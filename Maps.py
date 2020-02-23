import requests
from PIL import Image
from io import BytesIO


class Maps:
    def __init__(self):
        self.width_map, self.height_map = 650, 450
        self.toponym_to_find = "Владивосток"
        self.mapstyle = 'map'
        self.point = ''
        self.delta = 17
        self.find_coords()
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
        self.coords = response_geo.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split()
        self.coords = [float(i) for i in self.coords]
        self.address = response_geo.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]["formatted"]
        if "postal_code" in  response_geo.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]:
            self.postal_code = response_geo.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
        else:
            self.postal_code = ''

    def image_map(self):
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        map_params = {
            "ll": ','.join([str(self.coords[0]), str(self.coords[1])]),
            "z": str(self.delta),
            "l": self.mapstyle,
            'size': f'{self.width_map},{self.height_map}',
            "pt": self.point
        }
        response_api = requests.get(map_api_server, params=map_params)
        if not response_api:
            raise Exception
        return Image.open(BytesIO(response_api.content)).convert('RGBX').tobytes()

    def map_moving(self, way):
        if way == "pg_up" and self.delta != 17:
            self.delta += 1
        elif way == "pg_down" and self.delta != 0:
            self.delta -= 1
        elif way == 'up':
            self.coords[1] = self.coords[1] + 0.000007988506000377322 * self.height_map * 2 ** (17 - self.delta)
        elif way == 'down':
            self.coords[1] = self.coords[1] - 0.000007988506000377322 * self.height_map * 2 ** (17 - self.delta)
        elif way == 'right':
            self.coords[0] = self.coords[0] + 0.000010688212998736789 * self.width_map * 2 ** (17 - self.delta)
        elif way == 'left':
            self.coords[0] = self.coords[0] - 0.000010688212998736789 * self.width_map * 2 ** (17 - self.delta)

    def find_object(self, object):
        self.toponym_to_find = object
        self.find_coords()
        self.point = ','.join([str(self.coords[0]), str(self.coords[1]), 'flag'])

    def find_point(self):
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": self.point[:-5],
            "format": "json"}
        response_geo = requests.get(geocoder_api_server, params=geocoder_params)
        if not response_geo:
            raise Exception
        self.address = response_geo.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]["formatted"]
        if "postal_code" in response_geo.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]:
            self.postal_code = response_geo.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
        else:
            self.postal_code = ''

    def set_point(self, x, y):
        self.x = self.coords[0] + 0.000010688212998736789 * x * 2 ** (17 - self.delta)
        self.y = self.coords[1] - 0.000007988506000377322 * y * 2 ** (17 - self.delta)

