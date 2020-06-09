import numpy as np
import json
from ._base_map import BaseMap
from .single_terrain import SingleTerrain
from gibbon.web_api import MapBox
from gibbon.utility import convert


# TODO:将场地生成的方式转换为多线程异步


class TerrainMap(BaseMap):
    def __init__(self, coords: list, radius: float = 2000, level: int = 16):
        super().__init__(coords, radius, level)
        self.requester = MapBox()
        self.tensor = list()

    def load_tensor(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.tensor = list(map(np.array, data))

    def dump_tensor(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            data = list(map(lambda x: x.tolist(), self.tensor))
            json.dump(data, f, ensure_ascii=False)

    def calculate_tensor(self):
        self.tensor = list()

        for index in self.indices:
            status = True
            
            while status:
                try:
                    data = self.requester.terrain_matrix_by_tile_index(index)
                    self.tensor.append(data)
                    status = False

                except Exception as e:
                    print(e)
                    print('retrying...')

    def create_tiles(self, density=10):
        self.tiles = list()

        for i in range(len(self.tensor)):
            matrix = self.tensor[i]
            index = self.indices[i]
            st = SingleTerrain(matrix, density, self.tile_size)
            diss  = [
                (index[1] - self.center_xyz[1]) * self.tile_size,
                (index[0] - self.center_xyz[0]) * self.tile_size,
            ]
            st.move(diss)
            self.tiles.append(st)
