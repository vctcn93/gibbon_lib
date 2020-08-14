import json
import numpy as np
from gibbon.maps import MapSensor, BaseTile


class BaseMap:
    def __init__(self, map_sensor):
        self.map_sensor = map_sensor
        self._tiles = np.array([])

    @property
    def shape(self):
        return self._tiles.shape

    @property
    def tiles(self):
        return self._tiles.tolist()

    @property
    def _mesh(self):
        if len(self.tiles) > 0:
            return np.vectorize(lambda x: x.mesh)(self._tiles)
        return np.array([])

    @property
    def mesh(self):
        meshes = self._mesh.copy()

        if len(self._mesh) > 0:
            meshes = meshes.reshape(self.shape[0] * self.shape[1])

        return meshes.tolist()

    def dump_mesh(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.mesh, f, ensure_ascii=False)

    def create(self):
        f = lambda x: BaseTile(x, self.map_sensor.center_index)
        self._tiles = np.apply_along_axis(f, 2, self.map_sensor._indices)


if __name__ == '__main__':
    cs = [112.970840, 28.198560]
    msensor = MapSensor(cs, 2000)
    bmap = BaseMap(msensor)
    print(bmap.mesh, len(bmap.mesh))
    bmap.create()
    print(bmap._tiles.shape, bmap.tiles)
    print(bmap.mesh, len(bmap.mesh))
