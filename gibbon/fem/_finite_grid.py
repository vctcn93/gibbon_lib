import json
import numpy as np
from shapely.geometry import LineString
import gibbon.geometry.vector_math as vmath


class FiniteGrid:
    quantity_limit = 1000

    def __init__(self, polyline: list, density: float = 1):
        self._polyline = np.array(polyline)
        self._density = density

        self.score_points = list()
        self._subjects = set()
        self.added = list()

        self.cells = list()
        self.setup()

    @property
    def polyline(self):
        return self._polyline.tolist()

    @property
    def density(self):
        return self._density

    @property
    def quantity(self):
        return self._quantity

    @property
    def subjects(self):
        return self._subjects

    @property
    def scores(self):
        return [cell.score for cell in self.cells]

    @property
    def mesh(self):
        return [c.mesh for c in self.cells]

    @staticmethod
    def divide_by_quantity(quantity):
        ls = list(range(quantity))
        new = [0] * quantity

        for i in range(quantity):
            new[i] = ls[i] / (quantity - 1)

        return new

    def set_quantity_limit(self, value):
        self.quantity_limit = value
        self.setup()

    def set_polyline(self, polyline):
        self._polyline = np.array(polyline)
        self.setup()

    def set_density(self, density):
        self._density = density
        self.setup()

    def add_score_point(self, score_point):
        if score_point.uuid not in self.added:
            self.added.append(score_point.uuid)
            self.score_points.append(score_point)
            self._subjects |= {score_point.type}

    def add_score_points(self, score_points):
        for sp in score_points:
            self.add_score_point(sp)

    def subject_score(self, key):
        return [cell.subject_score(key) for cell in self.cells]

    def compute(self):
        for cell in self.cells:
            cell._scores = dict()
            cell._forbidden = dict()

            for score_point in self.score_points:
                score_point.compute(cell)

    def setup(self):
        self._quantity = int(self.quantity_limit * self._density)
        self.geo = LineString(self._polyline)

    def dump_mesh(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.mesh, f)
