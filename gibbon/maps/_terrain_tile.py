import numpy as np
from gibbon.maps import BaseTile


class TerrainTile(BaseTile):
    row_limit = 10

    def __init__(self, origin, tile_index, matrix, density=1):
        self._matrix = np.array(matrix)
        self._density = density
        super().__init__(origin, tile_index)

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
    def vertices(self):
        return self._vertices.tolist()

    @staticmethod
    def height_by_rgb(r, g, b, unit='mm'):
        a = - 10000 + ((r * 256 * 256 + g * 256 + b) * 0.1)
        return a * 1000 if unit == 'mm' else a

    def calculate_row_quantity(self):
        self._row_quantity = int(self.row_limit * self._density)

    def calculate_vertices_indices(self):
        width, height, deep = self._matrix.shape
        wgap, hgap = int(width / self._row_quantity), int(height / self._row_quantity)

        indices = list()

        for i in range(self._row_quantity - 1):
            for j in range(self._row_quantity - 1):
                indices.append([i*wgap, j*hgap])
            indices.append([i*wgap, height-1])

        for i in range(self._row_quantity - 1):
            indices.append([width-1, i*hgap])
        indices.append([width-1, height-1])

        self._vertices_indices = np.array(indices)

    def calculate_heights(self):
        r, g, b = self._matrix[:, :, 0], self._matrix[:, :, 1], self._matrix[:, :, 2]
        self._heights = np.vectorize(self.height_by_rgb)(r, g, b)

    def calculate_faces(self):
        result = list()

        for i in range(self._row_quantity, self._row_quantity ** 2):
            if i % self._row_quantity != self._row_quantity - 1:
                result.append(
                    [i - self._row_quantity, i, i + 1, i - self._row_quantity + 1]
                )

        self.faces = result

    def calculate_vertices(self):
        unit = self._tile_size / (self._matrix.shape[0] - 1)
        coords = self._vertices_indices * unit
        coords += self._coords - [self._tile_size / 2, self._tile_size / 2]
        coords = np.array(coords)
        k = np.array(self.heights)
        k = k.reshape([len(k), 1])
        self._vertices = np.concatenate((coords, k), axis=1)

    def set_colour(self, colour):
        self.colours = [colour] * len(self.vertices)

    def create(self):
        super().create()
        self.calculate_row_quantity()
        self.calculate_vertices_indices()
        self.calculate_heights()
        self.calculate_faces()
        self.calculate_vertices()
        self.set_colour([255, 255, 255])
        self._mesh['v'] = self.vertices
        self._mesh['f'] = self.faces
        self._mesh['c'] = self.colours


if __name__ == '__main__':
    import json

    path = r'C:\Users\wenhs\Desktop\tensor_backup.json'
    p2 = r'C:\Users\wenhs\Desktop\ttile.json'

    with open(path, 'r', encoding='utf-8') as f:
        tensor = json.load(f)

    matrix = tensor[0]
    cs = [112.970840, 28.198560]
    tile_index = [106667, 54827, 17]

    ttile = TerrainTile(cs, tile_index, matrix)
    print(ttile.vertices)
    ttile.dump_mesh(p2)
