from gibbon.maps import BaseMap, TerrainTile
from gibbon.web_api import MapBox
from threading import Thread, Lock
import json
import time


class TerrainMap(BaseMap):
    thread_limit = 20

    def __init__(self, map_sensor):
        self.web_api = MapBox()
        self.tensor = dict()

        self.thread_count = 0
        self.lock = Lock()
        super().__init__(map_sensor)

    @property
    def loaded_indices(self):
        return list(self.tensor.keys())

    @property
    def current(self):
        return list(self._tiles.keys())

    @property
    def tiles(self):
        return list(self._tiles.values())

    def dump_tensor(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.tensor, f)

    def load_tensor(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.tensor = data

    def create_tiles(self):
        self._tiles = dict()

        for tile_index in self.map_sensor.tile_indices:
            index = tuple(tile_index)

            if index in self.loaded_indices:
                matrix = self.tensor[index]
                self._tiles[index] = TerrainTile(self.map_sensor.origin,
                    tile_index,
                    matrix
                )

            else:
                thread = Thread(target=self._create_tile_async, args=[tile_index, TerrainTile])
                thread.start()

    def _create_tile_async(self, tile_index: tuple, callback, density=1):
        while self.thread_count > self.thread_limit:
            time.sleep(.02)

        with self.lock:
            self.thread_count += 1

        status = True

        while status:
            try:
                matrix = self.web_api.terrain_matrix_by_tile_index(tile_index)
                status = False

            except Exception as e:
                print(e)
                print('- connection exceeded limit at thread_count=', self.thread_count)
                time.sleep(.02)

        obj = callback(
            self.map_sensor.origin,
            tile_index,
            matrix,
            density 
        )

        index = tuple(tile_index)
        self.tensor[index] = matrix
        self._tiles[index] = obj

        with self.lock:
            self.thread_count -= 1

        time.sleep(.01)
