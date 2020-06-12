import numpy as np
from gibbon.maps import BaseTile
from gibbon.utility import timeit, Convert


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
            self._vertices_indices[:, 0],
            self._vertices_indices[:, 1],
        ].tolist()

    @property
    def faces(self):
        return self._faces.tolist()

    @property
    def colours(self):
        return self._colours

    @property
    def vertices(self):
        return self._vertices.tolist()

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
        vertices_indices = indices.T
        shape = vertices_indices.shape
        self._vertices_indices = vertices_indices.reshape([shape[0]*shape[1], shape[2]])

    def calculate_heights(self):
        r, g, b = self._matrix[:, :, 0], self._matrix[:, :, 1], self._matrix[:, :, 2]
        self._heights = np.vectorize(self.height_by_rgb)(r, g, b)

    def calculate_faces(self):
        result = list()
        basic = np.array([0, self._row_quantity, self._row_quantity + 1, 1])

        for i in range(self._row_quantity - 1):
            for j in range(self._row_quantity - 1):
                param = i * 10 + j
                c = basic + param
                result.append(c)

        self._faces = np.array(result)

    def calculate_vertices(self):
        unit = self._tile_size / (self._matrix.shape[0] - 1)
        coords = self._vertices_indices * unit
        coords += self._coords - [self._tile_size / 2, self._tile_size / 2]
        k = np.expand_dims(np.array(self.heights), axis=1)
        self._vertices = np.concatenate((coords, k), axis=1)

    def set_colour(self, colour):
        self._colours = [colour] * len(self.vertices)
        self._mesh['c'] = self.colours

    @timeit
    def setup(self):
        super().setup()
        self.calculate_row_quantity()
        self.calculate_vertices_indices()
        self.calculate_heights()
        self.calculate_faces()
        self.calculate_vertices()
        self._mesh['v'] = self.vertices
        self._mesh['f'] = self.faces
        self.set_colour([255, 255, 255])


if __name__ == '__main__':
    import json

    path = r'C:\Users\wenhs\Desktop\tensor_backup.json'
    p2 = r'C:\Users\wenhs\Desktop\ttile.json'

    with open(path, 'r', encoding='utf-8') as f:
        tensor = json.load(f)

    matrix = tensor[0]
    cs = [112.970840, 28.198560]
    center_tile_index = Convert.lnglat_to_tile_index(cs, 17)
    tile_index = [106667, 54827, 17]

    ttile = TerrainTile(center_tile_index, tile_index, matrix)
    print(ttile.mesh)
    ttile.dump_mesh(p2)
