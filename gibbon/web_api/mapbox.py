from .keys import MAPBOX_KEY
import requests
import numpy as np
from PIL import Image
from io import BytesIO


class MapBox:
    def __init__(self, key=MAPBOX_KEY):
        self.key = key

    def set_key(self, key):
        self.key = key

    def terrain_matrix_by_tile_index(self, tile_index, show=False):
        x, y, z = tile_index
        url = f'https://api.mapbox.com/v4/mapbox.terrain-rgb/{z}/{x}/{y}@2x.png'
        params = {'access_token': self.key}
        response = requests.get(url, params=params)
        img = Image.open(BytesIO(response.content))

        if show:
            img.show()

        rgb = img.convert('RGB')
        return np.array(rgb).astype(int)

    def light_matrix_by_tile_index(self, tile_index, show=False):
        x, y, z = tile_index
        url = f'https://b.tiles.mapbox.com/v4/mapquest.light-mb/{z}/{x}/{y}@2x.png?'
        params = {'access_token': self.key}
        response = requests.get(url, params=params)
        img = Image.open(BytesIO(response.content))

        if show:
            img.show()

        rgb = img.convert('RGB')
        return np.array(rgb).astype(int)
