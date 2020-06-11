from ._finite_cell import FiniteCell
from ._finite_grid import FiniteGrid
import gibbon.geometry.vector_math as vmath


class LineBasedFiniteGrid(FiniteGrid):
    def __init__(
        self,
        polyline: list,
        density: float
    ):
        super().__init__(polyline, density)

    def setup(self):
        super().setup()
        params = self.divide_by_quantity(self._quantity)
        points = list()

        points = [
            vmath.point_at_parameter_polyline(
                self._polyline, param
            ) for param in params
        ]
        size = self.geo.length / self._quantity
        self.cells = [FiniteCell(point, size) for point in points]
