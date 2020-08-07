import json
import numpy as np
from gibbon.utility import Convert


class BaseTile:
    def __init__(self, origin_tile_index, tile_index):
        self._origin_tile_index = np.array(origin_tile_index)
        self._tile_index = np.array(tile_index)
        self.setup()

    @property
    def origin_tile_index(self):
        return tuple(self._origin_tile_index.tolist())

    @property
    def tile_size(self):
        return self._tile_size

    @property
    def tile_index(self):
        return tuple(self._tile_index.tolist())

    @property
    def level(self):
        return int(self._tile_index[2])

    @property
    def coords(self):
        return self._coords.tolist()

    @property
    def mesh(self):
        return self._mesh

    def calculate_tile_size(self):
        self._tile_size = Convert.tile_size_by_zoom(self.level)

    def calculate_coords(self):
        # ! How to rotate it?
        diss = self._tile_index - self._origin_tile_index
        coords = self._tile_size * diss
        self._coords = np.flip(coords[:-1])

    def create_mesh(self):
        self._mesh = {
            'tp': 'mesh',
            'v': [[]],
            'f': [[]],
            'c': [[]]
        }

    def set_origin(self, origin):
        self._origin = np.array(origin)
        self.setup()

    def set_tile_index(self, tile_index):
        self._tile_index = np.array(tile_index)
        self.setup()

    def setup(self):
        self.calculate_tile_size()
        self.calculate_coords()
        self.create_mesh()

    def dump_mesh(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.mesh, f)


if __name__ == '__main__':
    cs = [112.970840, 28.198560]
    center_tile_index = Convert.lnglat_to_tile_index(cs, 17)
    # tile_index = [106667, 54827, 17]
    tile_index = [106666, 54826, 17]
    tile = BaseTile(center_tile_index, tile_index)
    print(tile.tile_size)
    print(tile.coords)
