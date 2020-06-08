from shapely.geometry import Point, Polygon
import numpy as np


class Cell:
    def __init__(self, coords: list, size: float = 300.0):
        self._coords = np.array(coords).astype(float)
        self._size = size
        self._shape = None
        self._vertices = None
        self.colours = None

        self.geo_center = None
        self.geo = None

        self.create()
        self.set_colour([255, 255, 255])

    @property
    def coords(self):
        return self._coords.tolist()

    @property
    def shape(self):
        return self._shape.tolist()

    @property
    def vertices(self):
        return self._vertices.tolist()

    @property
    def size(self):
        return self._size

    @property
    def mesh(self):
        return {
            'tp': 'mesh',
            'v': self.vertices,
            'f': [[0, 1, 2, 3]],
            'c': self.colours
        }

    def create(self):
        corners = [
            [-self.size / 2, -self.size / 2],
            [self.size / 2, -self.size / 2],
            [self.size / 2, self.size / 2],
            [-self.size / 2, self.size / 2]
        ]
        shape = [self._coords - corner for corner in corners]
        hs = np.zeros([len(shape), 1])
        self._shape = np.array(shape)
        self._vertices = np.concatenate((self._shape, hs), axis=1)

        self.geo_center = Point(self._coords)
        self.geo = Polygon(self._shape)

    def set_colour(self, rgb: list):
        self.colours = [[rgb]] * len(self.vertices)

    def move(self, vector: list):
        self._coords += vector
        self.create()

    def set_coords(self, coords):
        self._coords = np.array(coords)
        self.create()

    def set_size(self, size):
        self.size = size
        self.create()
