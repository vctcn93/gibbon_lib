import numpy as np
import scipy.spatial as sp


class Cell:
    def __init__(self, coords: list, size: float):
        self.size = size
        self._coords = self.create_coords(coords)
        self._vertices = self.calculate_vertices(self._coords)
        self.faces = [[0, 1, 2, 3]]
        self.set_colour([255, 255, 255])

    @property
    def coords(self) -> list:
        return self._coords.astype(int).tolist()

    @property
    def vertices(self) -> list:
        return [v.astype(int).tolist() for v in self._vertices]

    @property
    def mesh(self) -> dict:
        return {
            'tp': 'mesh',
            'v': self.vertices,
            'f': self.faces,
            'c': self.colours
        }

    def create_coords(self, coords):
        order = [
            [-self.size / 2, -self.size / 2],
            [self.size / 2, -self.size / 2],
            [self.size / 2, self.size / 2],
            [-self.size / 2, self.size / 2]
        ]
        return np.array([np.array(coords) + np.array(od) for od in order])

    def calculate_vertices(self, coord) -> list:
        hs = np.zeros([len(coord), 1]).astype(int)
        return np.concatenate((coord, hs), axis=1)

    def set_colour(self, rgb: list):
        self.colours = [rgb for i in range(len(self._vertices))]

    def move(self, vector):
        if isinstance(vector, list):
            vector = np.array(vector)
        self._coords += vector
        self._vertices = self.calculate_vertices(self._coords)


if __name__ == '__main__':
    c = Cell([0, 0], 10)
    assert c.coords == [[-5, -5], [5, -5], [5, 5], [-5, 5]]
    assert c.vertices == [[-5, -5, 0], [5, -5, 0], [5, 5, 0], [-5, 5, 0]]
    assert c.faces == [0, 1, 2, 3]
    assert c.colours == [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]]
    assert c.mesh == {
        'tp': 'mesh',
        'v': [[-5, -5, 0], [5, -5, 0], [5, 5, 0], [-5, 5, 0]],
        'f': [0, 1, 2, 3],
        'c': [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]]
    }
    c.set_colour([128, 128, 128])
    assert c.colours == [[128, 128, 128], [128, 128, 128], [128, 128, 128], [128, 128, 128]]
