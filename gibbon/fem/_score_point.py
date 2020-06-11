import uuid
import numpy as np
from shapely.geometry import Point, LineString
from ._finite_cell import FiniteCell


class ScorePoint:
    def __init__(
        self,
        coords: list,
        value: float = 1,
        influence_range: float = 2000
    ):
        self.uuid = str(uuid.uuid4())
        self.value = value

        self._coords = np.array(coords)
        self._influence_range = influence_range
        self.setup()

    @property
    def type(self):
        return self.__class__.__name__

    @property
    def coords(self):
        return self._coords.tolist()

    @property
    def influence_range(self):
        return self._influence_range

    def set_coords(self, coords):
        self._coords = np.array(coords)
        self.setup()

    def set_influence_range(self, influence_range):
        self._influence_range = influence_range
        self.setup()

    def setup(self):
        self.geo = Point(self._coords)
        self.buffer = self.geo.buffer(self._influence_range)

    def compute(self, obj: FiniteCell) -> float:
        if self.buffer.intersects(obj.geo_center):
            obj._scores[self.type] += self.value 


class Road(ScorePoint):
    def __init__(self, geometry, value, influence_range):
        ScorePoint.__init__(self, geometry, value, influence_range)

    def setup(self):
        self.geo = LineString(self._coords)
        self.buffer = self.geo.buffer(self._influence_range)

    def compute(self, obj: FiniteCell) -> float:
        if self.buffer.intersects(obj.geo_center):
            if self.value > obj._scores[self.type][0]:
                obj._scores[self.type] = [self.value] 


class Intersection(ScorePoint):
    def __init__(self, geometry, value, influence_range):
        ScorePoint.__init__(self, geometry, value, influence_range)

    def compute(self, obj: FiniteCell) -> float:
        if self.buffer.intersects(obj.geo_center):
            obj._forbidden[self.type].append(self.value)


class BusStop(ScorePoint):
    def __init__(self, geometry, value, influence_range):
        ScorePoint.__init__(self, geometry, value, influence_range)


class Metro(ScorePoint):
    def __init__(self, geometry, value, influence_range):
        ScorePoint.__init__(self, geometry, value, influence_range)


class UnderGround(ScorePoint):
    def __init__(self, geometry, value, influence_range):
        ScorePoint.__init__(self, geometry, value, influence_range)


class Pavement(ScorePoint):
    def __init__(self, geometry, value, influence_range):
        ScorePoint.__init__(self, geometry, value, influence_range)
