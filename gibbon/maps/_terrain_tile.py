import numpy as np
from scipy.spatial import distance as spd 
from gibbon.maps import BaseTile
from gibbon.utility import Convert


class TerrainTile(BaseTile):
    row_limit = 10

    def __init__(self, origin_tile_index, tile_index, matrix, density=1):
        self._matrix = np.array(matrix)
        self._density = density
        super().__init__(origin_tile_index, tile_index)

    @property
    def row_quantity(self):
        return self._row_quantity

    @property
    def matrix(self):
        return self._matrix.tolist()

    @property
    def density(self):
        return self._density

    @property
    def vertices_indices(self):
        return self._vertices_indices.tolist()

    @property
    def heights(self):
        return self._heights[
            self._vertices_indices.T[0],
            self._vertices_indices.T[1]
        ].tolist()

    @property
    def faces(self):
        return self._faces.reshape(-1, 4).tolist()

    @property
    def colours(self):
        return self._colours

    @property
    def vertices(self):
        return self._vertices.reshape(-1, 3).tolist()

    @staticmethod
    def height_by_rgb(r, g, b, unit='mm'):
        a = - 10000 + ((r * 256 * 256 + g * 256 + b) * .1)
        return a * 1000 if unit == 'mm' else a

    def calculate_row_quantity(self):
        a = int(self.row_limit * self._density)
        self._row_quantity = a if a < self._matrix.shape[0] else self._matrix.shape[0]

    def calculate_vertices_indices(self):
        column = np.linspace(0, self._matrix.shape[0]-1, self._row_quantity, dtype=int)
        row = np.linspace(0, self._matrix.shape[1]-1, self._row_quantity, dtype=int)
        indices = np.array(np.meshgrid(column, row))
        self._vertices_indices = indices.T

    def calculate_heights(self):
        r, g, b = self._matrix[:, :, 0], self._matrix[:, :, 1], self._matrix[:, :, 2]
        self._heights = np.vectorize(self.height_by_rgb)(r, g, b)
        # ! How to rotate it?
        # self._heights = np.rot90(self._heights, axes=(1, 0))

    def calculate_faces(self):
        basic = np.array([0, self._row_quantity, self._row_quantity + 1, 1])
        count = self._row_quantity - 1
        shape = [np.arange(count) + i * 10 for i in range(count)]
        self._faces = np.add.outer(shape, basic)

    def calculate_vertices(self):
        unit = self._tile_size / (self._matrix.shape[0] - 1)
        coords = self._vertices_indices * unit
        coords += self._coords - [self._tile_size / 2, self._tile_size / 2]
        self._vertices = np.stack((coords.T[0], coords.T[1], self.heights), axis=2)

    def set_colour(self, colour):
        self._colours = np.ones_like(self._vertices)
        self._mesh['c'] = self.colours

    def setup(self):
        super().setup()
        self.calculate_row_quantity()
        self.calculate_vertices_indices()
        self.calculate_heights()
        self.calculate_faces()
        self.calculate_vertices()
        self._mesh['v'] = self.vertices
        self._mesh['f'] = self.faces
