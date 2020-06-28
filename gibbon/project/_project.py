from gibbon.maps import MapSensor, TileMap, TerrainMap
from gibbon.fem import ShapeBasedFiniteGrid, LineBasedFiniteGrid
from gibbon.utility import Convert
from gibbon.web_api import Amap, Bmap
from shapely.geometry import Polygon
import pandas as pd


class Project:
    def __init__(
        self,
        polyline,
        origin,
        radius=2000,
        density=1
    ):
        self.sensor = MapSensor(origin, radius)
        self.tile_map = TileMap(self.sensor)
        self.terrain_map = TerrainMap(self.sensor)
        self.fem_red_line = LineBasedFiniteGrid(polyline, density)
        self.fem_site = ShapeBasedFiniteGrid(polyline, density)
        bounds = self.sensor.bounds
        line = [bounds[0], [bounds[1][0], bounds[0][1]], bounds[1], [bounds[0][0], bounds[1][1]]]
        self.fem_map = ShapeBasedFiniteGrid(line, density)
        self.amap = Amap()
        self.bmap = Bmap()

    def pois_by_keyword(self, keyword):
        llbounds = self.sensor.llbounds[0] + self.sensor.llbounds[1]
        return self.bmap.pois_by_keyword_bounds(keyword, llbounds)

    def setup(self):
        pass

    


if __name__ == '__main__':
    boundary = [
        [135645.11278065387, 32315.40416692337], 
        [135645.11278029159, 201671.17918046517], 
        [126952.82788838632, 211814.94409043854], 
        [85289.83720657602, 216309.82957304642], 
        [43411.964759724215, 217810.69178508036], 
        [-162833.7758713793, 217810.69178540818], 
        [-187833.77586947195, 192810.69178564614], 
        [-187833.77586565679, 142810.69178516977], 
        [-191333.77586374991, 112810.69178528897], 
        [-191333.77585802786, 13810.932417852804], 
        [-187710.77355013601, -17243.373066889122], 
        [-184568.05179033987, -74563.56585736759], 
        [-178656.31940851919, -122455.30853326805], 
        [-169447.6962624616, -182124.46695764549], 
        [-168331.07474528067, -212307.29579167254], 
        [-150410.09518061439, -328429.95081900246], 
        [-142375.37355051748, -357545.12295277603], 
        [-134252.77894793218, -410177.13715671189], 
        [-113968.53712664358, -423936.7188313175], 
        [-62660.312091929838, -412856.00462846644], 
        [-91011.301433665678, -165898.26749964245], 
        [135656.22394360788, -165898.26749976166], 
        [135656.22394360788, -115189.30818407424], 
        [126656.22394360788, -106189.30821271427], 
        [126686.89403142221, -97189.308212356642], 
        [57662.24364461191, -97189.308212356642], 
        [57461.112780706026, 32315.40416692337], 
        [135645.11278065387, 32315.40416692337]
    ]

    project = Project(boundary, origin=[113.520280, 22.130790])
    path = r'C:\Users\wenhs\Desktop'
    project.fem_red_line.dump_mesh(path + r'\fem_red_line.json')
    project.fem_site.dump_mesh(path + r'\fem_site.json')
    project.fem_map.dump_mesh(path + r'\fem_map.json')

    dfs = list()
    kinds = ['公交车站', '住宅']

    for k in kinds:
        pois = project.pois_by_keyword(k)
        location, names = pois['location'], pois['name']
        lnglats = location.apply(lambda x: [x['lng'], x['lat']])
        coords = lnglats.apply(
            lambda x: Convert.lnglat_to_mercator(x, project.sensor.origin)
        )

        rst = pd.DataFrame()
        rst['names'] = names
        rst['lnglat'] = lnglats
        rst['coords'] = coords
        rst.to_json(path + f'/{k}.json')
