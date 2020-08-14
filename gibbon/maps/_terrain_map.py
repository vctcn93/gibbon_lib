from gibbon.maps import BaseMap, TerrainTile
from gibbon.web_api import MapBox
from threading import Thread, Lock
import numpy as np
import json
import time


class TerrainMap(BaseMap):
    thread_limit = 20

    def __init__(self, map_sensor):
        self.web_api = MapBox()
        self.tensor = dict()
        self.created_tiles = dict()

        self.thread_count = 0
        self.lock = Lock()
        super().__init__(map_sensor)

    @property
    def loaded_tensor(self):
        return list(self.tensor.keys())

    def dump_tensor(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            data = {str(key): value.tolist() for key, value in self.tensor.items()}
            json.dump(data, f)

    def load_tensor(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            tensor = {eval(key): np.array(value) for key, value in data.items()}
            self.tensor = tensor

    def create(self):
        thread_list = list()
        created_tiles = list(self.created_tiles.keys())

        for row in self.map_sensor.indices:
            for tile_index in row:
                index = tuple(tile_index)

                if index not in created_tiles:
                    if index in self.loaded_tensor:
                        matrix = self.tensor[index]
                        self.created_tiles[index] = TerrainTile(
                            self.map_sensor.center_index,
                            tile_index,
                            matrix
                        )

                    else:
                        thread = Thread(target=self._create_tile_async, args=[tile_index, TerrainTile])
                        thread_list.append(thread)

        for t in thread_list:
            t.setDaemon(True)
            t.start()

        for t in thread_list:
            t.join()

        print(f'Finished >>> {len(thread_list)} tiles')

        f = lambda x: self.created_tiles[tuple(x)]
        self._tiles = np.apply_along_axis(f, 2, self.map_sensor._indices)

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
            self.map_sensor.center_index,
            tile_index,
            matrix,
            density 
        )

        index = tuple(tile_index)
        self.tensor[index] = matrix
        self.created_tiles[index] = obj

        with self.lock:
            self.thread_count -= 1

        time.sleep(.01)
        print(f'{tile_index} >>> Finished')
