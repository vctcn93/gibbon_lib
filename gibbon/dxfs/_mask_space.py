import numpy as np
import pandas as pd


class MaskSpace:
    def __init__(self, polygons, vector):
        polygons = np.array(polygons)
        self._polygons = sorted(polygons, key=lambda x: (np.sum(x, axis=1) / 4).tolist())
        self._vector = np.array(vector)
        self._original_data = list()
        self._core = pd.DataFrame()

    @property
    def vector(self):
        return self._vector.tolist()

    @property
    def base_point(self):
        arr = np.array(self._polygons)
        return [np.min(arr.T[0]), np.min(arr.T[1])]

    @property
    def data(self):
        self.manage_data()
        return self._core.copy()

    def manage_data(self):
        """
        update this.
        """
        pass
        
    def move(self):
        self._polygons += self._vector

    def get(self, texts):
        for geo in self._polygons:
            xmin, ymin = np.min(geo, axis=0)
            xmax, ymax = np.max(geo, axis=0)
            data = texts[
                    (texts['cad_x'] > xmin) &
                    (texts['cad_x'] < xmax) &
                    (texts['cad_y'] > ymin) &
                    (texts['cad_y'] < ymax) 
                ]
            data = data.drop_duplicates(subset=['cad_x', 'cad_y', 'text'])
            data = data.sort_values(by=['cad_x', 'cad_y'])
            data = data.reset_index()
            self._original_data.append(data)
