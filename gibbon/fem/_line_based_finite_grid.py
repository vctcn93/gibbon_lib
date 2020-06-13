import numpy as np
from gibbon.fem import FiniteCell
from gibbon.fem import FiniteGrid
import gibbon.geometry.vector_math as vmath


class LineBasedFiniteGrid(FiniteGrid):
    def __init__(
        self,
        polyline: list,
        density: float = 1
    ):
        super().__init__(polyline, density)

    def setup(self):
        super().setup()
        size = self.geo.length / self._quantity
        params = np.linspace(0, 1, self._quantity)

        def f(x):
            point = vmath.point_at_parameter_polyline(
                self._polyline, x
            )
            return FiniteCell(point, size)

        cells = np.vectorize(f)(params)
        self.cells = cells.tolist()


if __name__ == '__main__':
    lgrid = LineBasedFiniteGrid([[0, 0], [100, 100]])
    print(type(lgrid.cells))
    print(len(lgrid.cells))
