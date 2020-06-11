import numpy as np
from shapely.geometry import Polygon, Point
from ._finite_cell import FiniteCell
from ._finite_grid import FiniteGrid


class ShapeBasedFiniteGrid(FiniteGrid):
    def __init__(self, geometry, density):
        super().__init__(geometry, density)

    def setup(self):
        self._quantity = int(self.quantity_limit * self._density)
        self.geo = Polygon(self._polyline)
        self.cells = list()

        xmin, ymin, xmax, ymax = self.geo.bounds
        xdiss, ydiss = xmax - xmin, ymax - ymin
        size = np.sqrt(xdiss * ydiss / self._quantity)

        p_start = np.array([xmin, ymin])
        for i in range(int(xdiss / size)):
            for j in range(int(ydiss / size)):
                coords = p_start + [i * size, j * size]
                p = Point(coords)

                if self.geo.contains(p):
                    cell = FiniteCell(coords, size)
                    self.cells.append(cell)
