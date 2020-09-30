import numpy as np
import pandas as pd
from scipy.spatial import distance as spd
from gibbon.dxfs import MaskSpace


class MyMaskSpace(MaskSpace):
    def __init__(self, polygons, vector):
        super().__init__(polygons, vector)

    @staticmethod
    def get_distances(xs, ys):
        positions = np.array([xs, ys])
        distances = spd.cdist(positions.T, positions.T)
        return pd.DataFrame(distances)

    @staticmethod
    def check_index(dist, tor=2.25):
        length = 0
        indices = list()

        for i in range(len(dist)):
            data = dist.iloc[i]
            item = data[(data > 0) & (data < tor)]

            if len(item) > 0:
                length += 1
                indices.append(i)

        l = int(length / 2)
        return [[indices[i], indices[i + l]] for i in range(l)]

    @staticmethod
    def merge_labels_by_indices(df, indices):
        to_drop = list()

        for couple in indices:
            id1, id2 = couple[0], couple[1]
            to_drop.append(id2)
            value = df.iloc[id1]['text'] + df.iloc[id2]['text']
            df.set_value(id1, 'text', value)

        return df.drop(to_drop)

    @staticmethod
    def delevel_by_type(df):
        df['level'] = None
        t = df['type'].unique()

        for item in t:
            a = df[df['type'] == item]
            indices = list(range(len(a)))
            indices.reverse()

            for i in a.index:
                level = indices.pop()
                df['level'].iloc[i]= level

        return df

    def manage_data(self):
        ls = list()

        for i in range(0, len(self._original_data), 4):
            try:
                a = pd.DataFrame()

                types = self._original_data[i]['text'].values
                heights = self._original_data[i+1]['text'].values
                thickness = self._original_data[i+2]['text'].values
                x = self._original_data[i+3].iloc[1]['text']
                y = self._original_data[i+3].iloc[0]['text']

                if len(types) != len(heights):
                    df = self._original_data[i]
                    distances = self.get_distances(df['cad_x'], df['cad_y'])
                    indices = self.check_index(distances)
                    df = self.merge_labels_by_indices(df, indices)
                    self._original_data[i] = df
                    types = df['text'].values

                a['type'] = types
                a['height'] = heights
                a['thickness'] = thickness
                a['x'], a['y'] = x, y

                a = self.delevel_by_type(a)
                ls.append(a)

            except Exception as e:
                print(f'>>>> {i} error!', e)
                print(a)
                print(heights)

        self._core = pd.concat(ls, ignore_index=True)
