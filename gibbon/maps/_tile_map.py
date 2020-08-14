import numpy as np
from gibbon.maps import MapSensor, NormalTile, BaseMap


class TileMap(BaseMap):
    def __init__(self, map_sensor):
        super().__init__(map_sensor)

    def create(self):
        f = lambda x: NormalTile(x, self.map_sensor.center_index)
        self._tiles = np.apply_along_axis(f, 2, self.map_sensor._indices)


if __name__ == '__main__':
    cs = [112.970840, 28.198560]
    msensor = MapSensor(cs, 2000)
    tmap = TileMap(msensor)
    print(tmap.mesh, len(tmap.mesh))
    tmap.create()
    print(tmap._mesh, len(tmap._mesh))
    print(tmap.mesh, len(tmap.mesh))
