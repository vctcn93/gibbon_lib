import uuid
import numpy as np
import vector_math as vmath


class ScorePoint:
    def __init__(
        self,
        geometry: list = [[0, 0, 0]],
        value: float = 1,
        influence_range: float = 2000
    ):
        self.uuid = str(uuid.uuid4())
        self._geometry = np.array(geometry)
        self.value = value
        self.influence_range = influence_range
        self.type = self.__class__.__name__

    @property
    def geometry(self):
        return self._geometry.tolist()

    def compute_distance(self, obj: FiniteCell):
        return vmath.distance_point_point(self._geometry, obj._coords)

    def compute(self, obj: FiniteCell) -> float:
        distance = self.compute_distance(obj)

        if obj._scores.get(self.type) is None:
                obj._scores[self.type] = list()

        if distance <= self.influence_range:
            obj._scores[self.type].append(self.value)


class Road(ScorePoint):
    def __init__(self, geometry, value, influence_range):
        ScorePoint.__init__(self, geometry, value, influence_range)

    def compute_distance(self, obj):
        return vmath.distance_polyline_point(self.geometry, obj._coords)

    def compute(self, obj):
        distance = self.compute_distance(obj)

        if distance <= self.influence_range:
            obj._scores[self.type] = [self.value]


class Intersection(ScorePoint):
    def __init__(self, geometry, value, influence_range):
        ScorePoint.__init__(self, geometry, value, influence_range)

    def compute(self, obj: FiniteCell) -> float:
        distance = self.compute_distance(obj)

        if distance <= self.influence_range:
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
