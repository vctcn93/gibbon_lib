import numpy as np
from gibbon.maps import BaseTile
from gibbon.utility import Convert


class NormalTile(BaseTile):
    def __init__(self, origin_tile_index, tile_index):
        super().__init__(origin_tile_index, tile_index)

    @property
    def vertices(self):
        return self._vertices.tolist()

    def calculate_vertices(self):
        sizes = [[self.tile_size, self.tile_size]] * 4
        marks = np.array([[-1, -1], [1, -1], [1, 1], [-1, 1]])
        change = sizes * marks / 2
        coords = change + self._coords
        heights = np.zeros([len(coords), 1])
        self._vertices = np.concatenate((coords, heights), axis=1)

    def set_colour(self, colour):
        self._colour = np.ones_like(self._vertices)
        self._colour[:, :, :] = colour 

    def create_mesh(self):
        super().create_mesh()
        self.calculate_vertices()
        self._mesh['v'] = self.vertices
        self._mesh['f'] = [[0, 1, 2, 3]]
        # self._mesh['c'] = [[255, 255, 255]] * len(self._vertices)


if __name__ == '__main__':
    cs = [112.970840, 28.198560]
    center_tile_index = Convert.lnglat_to_tile_index(cs, 17)
    tile_index = [106667, 54827, 17]
    tile = NormalTile(center_tile_index, tile_index)
    print(tile.tile_size)
    print(tile.coords)
    print(tile.vertices)
    print(tile.mesh)
