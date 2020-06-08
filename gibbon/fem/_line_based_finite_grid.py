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
        self.score_points = list()
        self._subjects = set()
        self.added = list()

    @property
    def subjects(self):
        return self._subjects

    @property
    def scores(self):
        return [cell.score for cell in self.cells]

    def add_score_point(self, score_point):
        if score_point.uuid not in self.added:
            self.added.append(score_point.uuid)
            self.score_points.append(score_point)
            self._subjects |= {score_point.type}

    def add_score_points(self, score_points):
        for sp in score_points:
            self.add_score_point(sp)

    def compute(self):
        for cell in self.cells:
            cell._scores = dict()
            cell._forbidden = dict()

            for score_point in self.score_points:
                score_point.compute(cell)

    def subject_score(self, key):
        return [cell.subject_score(key) for cell in self.cells]

    def create(self):
        super().create()
        params = self.divide_by_quantity(self._quantity)
        points = list()

        points = [
            vmath.point_at_parameter_polyline(
                self._polyline, param
            ) for param in params
        ]
        size = self.geo.length / self._quantity
        self.cells = [FiniteCell(point, size) for point in points]
