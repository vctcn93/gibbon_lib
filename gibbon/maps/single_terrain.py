import numpy as np
import scipy.spatial as sp


class SingleTerrain:
    def __init__(self, matrix, density=10, size=1000, coords=[0, 0]):
        self.matrix = matrix
        self.density = density
        self.size = size
        self._indices = self.calculate_indices(matrix, density)
        self.coords = self._indices * self.size / (self.matrix.shape[0] - 1) - [self.size / 2 , self.size / 2]
        self._heights = self.calculate_heights(matrix, self._indices)
        self._vertices = None
        self.move(coords)
        self.faces = self.calculate_faces(density)
        self.colours = [[255, 255, 255] for i in range(len(self.vertices))]

    @property
    def indices(self):
        return self._indices.tolist()

    @property
    def heights(self):
        return self._heights.astype(int).tolist()

    @property
    def vertices(self):
        return self._vertices.astype(int).tolist()

    @property
    def mesh(self):
        return {
            'tp': 'mesh',
            'v': self.vertices,
            'f': self.faces,
            'c': self.colours
        }

    @staticmethod
    def height_by_rgb(r, g, b, unit='mm'):
        a = - 10000 + ((r * 256 * 256 + g * 256 + b) * 0.1)
        return a * 1000 if unit == 'mm' else a

    @staticmethod
    def calculate_indices(matrix, density):
        width, height, deep = matrix.shape
        wgap, hgap = int(width / density), int(height / density)

        indices = list()

        for i in range(density - 1):
            for j in range(density - 1):
                indices.append([i*wgap, j*hgap])
            indices.append([i*wgap, height-1])

        for i in range(density - 1):
            indices.append([width-1, i*hgap])
        indices.append([width-1, height-1])

        return np.array(indices)

    @staticmethod
    def calculate_vertices(heights, coords):
        heights = heights.copy()
        k = heights.reshape(len(heights), 1)
        return np.concatenate((coords, k), axis=1)

    @staticmethod
    def calculate_faces(density):
        result = list()

        for i in range(density, density ** 2):
            if i % 10 != 9:
                result.append([i - 10, i, i + 1, i - 9])

        return result

    def calculate_heights(self, matrix, indices):
        r, g, b = matrix[:, :, 0], matrix[:, :, 1], matrix[:, :, 2]
        heights = np.vectorize(self.height_by_rgb)(r, g, b)
        return heights[indices[:, 0], indices[:, 1]]

    def move(self, vector):
        if isinstance(vector, list):
            vector = np.array(vector)
        self.coords += vector
        self._vertices = self.calculate_vertices(self._heights, self.coords)
