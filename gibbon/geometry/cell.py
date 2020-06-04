import numpy as np
import scipy.spatial as sp


class Cell:
    def __init__(self, coords: list, size: float):
        self._coords = np.array(coords)
        self.size = size
        self._vertices = self.create_vertices()
        self.faces = [0, 1, 2, 3]
        self.set_colour([255, 255, 255])

    @property
    def coords(self) -> list:
        return self._coords.tolist()

    @property
    def vertices(self) -> list:
        return [v.tolist() for v in self._vertices]

    @property
    def mesh(self) -> dict:
        return {
            'tp': 'mesh',
            'v': self.vertices,
            'f': self.faces,
            'c': self.colours
        }

    def create_vertices(self) -> list:
        order = [
            [-self.size / 2, -self.size / 2],
            [self.size / 2, -self.size / 2],
            [self.size / 2, self.size / 2],
            [-self.size / 2, self.size / 2]
        ]
        return  [self._coords + np.array(od) for od in order]

    def set_colour(self, rgb: list):
        self.colours = [rgb for i in range(len(self._vertices))]


if __name__ == '__main__':
    c = Cell([0, 0], 10)
    assert c.vertices == [[-5, -5], [5, -5], [5, 5], [-5, 5]]
    assert c.faces == [0, 1, 2, 3]
    assert c.colours == [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]]
    assert c.mesh == {
        'tp': 'mesh',
        'v': [[-5, -5], [5, -5], [5, 5], [-5, 5]],
        'f': [0, 1, 2, 3],
        'c': [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]]
    }
    c.set_colour([128, 128, 128])
    assert c.colours == [[128, 128, 128], [128, 128, 128], [128, 128, 128], [128, 128, 128]]
