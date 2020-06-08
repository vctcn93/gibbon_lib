import json
import numpy as np
from shapely.geometry import LineString
import gibbon.geometry.vector_math as vmath


class FiniteGrid:
    quantity_limit = 1000

    def __init__(self, polyline: list, density: float):
        self._polyline = np.array(polyline)
        self._density = density
        self._quantity = None

        self.geo = None
        self.cells = list()
        self.create()

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
        self.create()

    def set_polyline(self, polyline):
        self._polyline = np.array(polyline)
        self.create()

    def set_density(self, density):
        self._density = density
        self.create()

    def create(self):
        self._quantity = int(self.quantity_limit * self._density)
        self.geo = LineString(self._polyline)

    def dump_mesh(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.mesh, f)

