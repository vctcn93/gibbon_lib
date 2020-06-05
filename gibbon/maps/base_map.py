from gibbon.utility import convert
from gibbon.geometry import Cell
import json


class BaseMap:
    def __init__(self, coords: list, radius: float = 2000, level: int = 16):
        self.origin = coords
        self.coords = coords
        self.radius = radius
        self.level = level
        self.tile_size = convert.tile_size_by_zoom(level)
        self.center_xyz = convert.lnglat_to_tile_index(coords, level)
        self.indices = convert.indices_by_lnglat_level_radius(coords, level, radius)
        self.tiles = list()

    @property
    def mesh(self):
        return [st.mesh for st in self.tiles] 

    def create_tiles(self):
        self.tiles = list()

        for i in range(len(self.indices)):
            index = self.indices[i]
            c = Cell([0, 0], self.tile_size)
            diss  = [
                (index[1] - self.center_xyz[1]) * self.tile_size,
                (index[0] - self.center_xyz[0]) * self.tile_size,
            ]
            c.move(diss)
            self.tiles.append(c)

    def dump_mesh(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.mesh, f, ensure_ascii=False)
