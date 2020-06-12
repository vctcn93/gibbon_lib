from gibbon.maps import MapSensor, NormalTile, BaseMap


class TileMap(BaseMap):
    def __init__(self, map_sensor):
        super().__init__(map_sensor)

    def create_tiles(self):
        self._tiles = [
            NormalTile(self.map_sensor.center_index, index) for index in self.map_sensor.tile_indices
        ]


if __name__ == '__main__':
    cs = [112.970840, 28.198560]
    msensor = MapSensor(cs, 2000)
    tmap = TileMap(msensor)
    print(tmap.mesh, len(tmap.mesh))
    tmap.create_tiles()
    print(tmap.mesh, len(tmap.mesh))
