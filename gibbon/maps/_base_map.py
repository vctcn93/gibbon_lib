import json
from gibbon.maps import MapSensor, BaseTile


class BaseMap:
    def __init__(self, map_sensor):
        self.map_sensor = map_sensor
        self._tiles = list()
        self.create_tiles()

    @property
    def tiles(self):
        return self._tiles

    @property
    def mesh(self):
        return [tile.mesh for tile in self.tiles]

    def dump_mesh(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.mesh, f, ensure_ascii=False)

    def create_tiles(self):
        self._tiles = [
            BaseTile(self.map_sensor.origin, index) for index in self.map_sensor.tile_indices
        ]


if __name__ == '__main__':
    cs = [112.970840, 28.198560]
    msensor = MapSensor(cs, 2000)
    bmap = BaseMap(msensor)
    print(bmap.mesh, len(bmap.mesh))
