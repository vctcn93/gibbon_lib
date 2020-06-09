import numpy as np
from gibbon.utility import Convert


class MapSensor:
    row_limit = 6

    def __init__(self, lnglat, radius):
        self._lnglat = np.array(lnglat)
        self._radius = radius
        self.create()

    @property
    def origin(self):
        return self._lnglat.tolist()

    @property
    def radius(self):
        return self._radius

    @property
    def level(self):
        return self._level

    @property
    def tile_size(self):
        return self._tile_size

    @property
    def center_index(self):
        return self._center_index.tolist()

    @property
    def tile_indices(self):
        return self._tile_indices.tolist()

    def set_lnglat(self, lnglat):
        self._lnglat = np.array(lnglat)
        self.create()

    def set_raidus(self, radius):
        self._radius = radius
        self.create()

    def set_row_limit(self, value):
        self.row_limit = value
        self.create()

    def calculate_level(self):
        disses = list()

        for i in range(10, 19):
            size = Convert.tile_size_by_zoom(i, 'm')
            quantity = self._radius / size
            diss = abs(quantity - self.row_limit)
            disses.append(diss)

        minimum = min(disses)
        index = disses.index(minimum)

        self._level = 10 + index

    def calculate_tile_size(self):
        self._tile_size = Convert.tile_size_by_zoom(self._level)

    def calculate_center_index(self):
        center_index = Convert.lnglat_to_tile_index(self._lnglat, self._level)
        self._center_index = np.array(center_index)

    def calculate_tile_indices(self):
        result = list()

        x, y, z = self.center_index
        xstart, ystart = x - int(self.row_limit / 2), y - int(self.row_limit / 2)

        for i in range(int(self.row_limit)):
            for j in range(int(self.row_limit)):
                result.append([int(xstart + i), int(ystart + j), z])

        self._tile_indices = np.array(result)

    def create(self):
        self.calculate_level()
        self.calculate_tile_size()
        self.calculate_center_index()
        self.calculate_tile_indices()


if __name__ == '__main__':
    cs = [112.970840, 28.198560]
    msensor = MapSensor(cs, 2000)
    print(msensor.level)
    print(msensor.tile_size)
    print(msensor.tile_indices)
    print(msensor.center_index)
    print(len(msensor.tile_indices))
    print(msensor.tile_indices.index(msensor.center_index))