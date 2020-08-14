import uuid
import json
import pandas as pd
import numpy as np
from gibbon.utility import Convert


class Buildings:
    def __init__(self, sensor, path=None):
        self.sensor = sensor
        self.df = None
        self.selected = None

        if path:
            self.load_dataframe(path)

    def load_dataframe(self, path):
        buildings = list()

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            features = data['features']

            for f in features:
                try:
                    floors = f['properties']['Floor']
                    coords = f['geometry']['coordinates'][0][0][:-1]
                    building = {'coords': coords, 'floors': floors}
                    buildings.append(building)

                except Exception as e:
                    pass

        uids = [uuid.uuid4() for i in range(len(buildings))]
        df = pd.DataFrame(buildings, index=uids)

        f = np.vectorize(lambda a, b: np.average(np.array(a), axis=0).tolist()[b])
        df['lng'], df['lat'] = f(df['coords'], 0), f(df['coords'], 1)
        self.df = df

    def create(self):
        def f(lnglats):
            return [Convert.lnglat_to_mercator(ll, self.sensor.origin) for ll in lnglats]

        if self.df is not None:
            selected = self.df[
                (self.df['lng'] > self.sensor.llbounds[0][0]) &
                (self.df['lng'] < self.sensor.llbounds[1][0]) &
                (self.df['lat'] > self.sensor.llbounds[0][1]) &
                (self.df['lat'] < self.sensor.llbounds[1][1])
            ]

            selected['position'] = selected['coords'].apply(f)
            selected['height'] = selected['floors'] * 3000
            self.selected = selected

    @property
    def extrusion(self):
        return [
            {
                'tp': 'extrude',
                'l': data['position'],
                'h': data['height']
            } for i, data in self.selected.iterrows()
        ]

    def dump_extrusion(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.extrusion, f)


if __name__ == '__main__':
    from gibbon.maps import MapSensor

    path = r'F:\02_projects\YangDaShiTouBiao\geojson\Changsha.geojson'
    path_out = r'F:\02_projects\YangDaShiTouBiao\geojson\YangDaShiTouBiao.json'
    origin = [113.058780, 28.201170]
    radius = 2000

    sensor = MapSensor(origin, radius)
    bmap = Buildings(sensor, path)
    print(bmap.df)
    bmap.create()
    bmap.dump_extrusion(path_out)
