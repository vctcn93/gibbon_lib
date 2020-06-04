from finite_cell import FiniteCell
import vector_math as vmath


class LineBasedFiniteGrid:
    quantity_limit = 1000

    def __init__(
        self,
        curve: list,
        density: float,
        line_width: float=10
    ):
        self.curve = curve
        self.density = density
        self.line_width = line_width
        self.score_points = list()
        self.cells = self.create_cells()
        self._subjects = set()
        self.added = list()

    def create_cells(self):
        quantity = int(self.density * self.quantity_limit)
        length = vmath.length_of_polyline(self.curve)
        unit = length / quantity
        coords = [vmath.point_at_parameter_polyline(self.curve, t*unit) for t in range(quantity)]
        return [
            FiniteCell(coord, unit) for coord in coords
        ]

    @property
    def subjects(self):
        return self._subjects

    @property
    def quantity(self):
        return len(self.cells)

    @property
    def scores(self):
        return [cell.score for cell in self.cells]

    @property
    def meshes(self):
        return [cell.mesh for cell in self.cells]

    @classmethod
    def set_quantity_limited(cls, value):
        cls.quantity_limit = value

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
