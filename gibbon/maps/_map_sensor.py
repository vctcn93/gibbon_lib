import numpy as np
from gibbon.utility import Convert


class MapSensor:
    row_limit = 7

    def __init__(self, lnglat, radius):
        self._lnglat = np.array(lnglat)
        self._radius = radius
        self.setup()

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
    def indices(self):
        return self._indices.tolist()

    @property
    def shape(self):
        return self._indices.shape

    @property
    def bounds(self):
        return self._bounds.tolist()

    @property
    def llbounds(self):
        return self._llbounds

    def set_lnglat(self, lnglat):
        self._lnglat = np.array(lnglat)
        self.setup()

    def set_raidus(self, radius):
        self._radius = radius
        self.setup()

    def set_row_limit(self, value):
        self.row_limit = value
        self.setup()

    def calculate_level(self):
        levels = np.arange(10, 19).astype(float)

        def f(x): 
            size = Convert.tile_size_by_zoom(x, 'm') 
            quantity = self._radius / size 
            return abs(quantity - self.row_limit) 

        disses = np.vectorize(f)(levels)
        self._level = int(10 + np.argmin(disses))

    def calculate_tile_size(self):
        self._tile_size = Convert.tile_size_by_zoom(self._level)

    def calculate_center_index(self):
        center_index = Convert.lnglat_to_tile_index(self._lnglat, self._level)
        self._center_index = np.array(center_index)

    def calculate_indices(self):
        x, y, z = self.center_index
        diss = self.row_limit / 2
        xs = np.arange(x - diss + 1, x + diss + 1)
        ys = np.arange(y - diss + 1, y + diss + 1)
        grid = np.meshgrid(xs, ys)

        zs = np.zeros_like(grid[0])
        zs[:] = z
        grid.append(zs)

        self._indices = np.array(grid).astype(int).T

    def calculate_bounds(self):
        extremums = [
            np.min(self._indices, axis=(0, 1)),
            np.max(self._indices, axis=(0, 1))
        ]
        diss = extremums - self._center_index
        bounds = diss * self._tile_size
        fix = [
            [-self._tile_size, -self._tile_size, 0], 
            [self._tile_size, self._tile_size, 0]
        ]
        bounds += fix
        self._bounds = np.delete(bounds, -1, axis=1)
        self._llbounds = list(
            map(
                lambda x: Convert.mercator_to_lnglat(x, self.origin),
                self._bounds / 1000
            )
        )

    def setup(self):
        self.calculate_level()
        self.calculate_tile_size()
        self.calculate_center_index()
        self.calculate_indices()
        self.calculate_bounds()


if __name__ == '__main__':
    origin=[113.520280, 22.130790]
    msensor = MapSensor(origin, 2000)
    print(msensor.level)
    print(msensor.tile_size)
    print(msensor.indices)
    print(msensor.center_index)
    print(len(msensor.indices))
    print(msensor.bounds)
    print(msensor.llbounds)
