import json
import numpy as np
from gibbon.utility import Convert


class BaseTile:
    def __init__(self, origin, tile_index):
        self._origin = np.array(origin)
        self._tile_index = np.array(tile_index)
        self.create()

    @property
    def tile_size(self):
        return self._tile_size

    @property
    def tile_index(self):
        return self._tile_index.tolist()

    @property
    def level(self):
        return int(self._tile_index[2])

    @property
    def coords(self):
        return self._coords.tolist()

    @property
    def lnglat(self):
        return self._lnglat.tolist()

    @property
    def mesh(self):
        return self._mesh

    def calculate_tile_size(self):
        self._tile_size = Convert.tile_size_by_zoom(self.level)

    def calculate_coords(self):
        lnglat = Convert.tile_index_to_lnglat(self._tile_index)
        coords = Convert.lnglat_to_mercator(lnglat, self._origin)
        self._coords = np.array(
            [coords[0] + self._tile_size / 2, coords[1] - self._tile_size / 2]
        )

    def calculate_lnglat(self):
        lnglat = Convert.mercator_to_lnglat(self._coords / 1000, self._origin)
        self._lnglat = np.array(lnglat)

    def create_mesh(self):
        self._mesh = {
            'tp': 'mesh',
            'v': [[]],
            'f': [[]],
            'c': [[]]
        }

    def create(self):
        self.calculate_tile_size()
        self.calculate_coords()
        self.calculate_lnglat()
        self.create_mesh()

    def dump_mesh(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.mesh, f)


if __name__ == '__main__':
    cs = [112.970840, 28.198560]
    tile_index = [106667, 54827, 17]
    tile = BaseTile(cs, tile_index)
    print(tile.tile_size)
    print(tile.coords)
    print(tile.lnglat)
