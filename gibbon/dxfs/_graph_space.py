import ezdxf
import pandas as pd


class GraphSpace:
    def __init__(self, path):
        doc = ezdxf.readfile(path)
        self.msp = doc.modelspace()

    def load_texts(self):
        texts = self.msp.query('TEXT')
        tdata = list()

        for t in texts:
            coords = list(t.dxf.insert)[:-1]
            text = t.dxf.text

            if text not in ('', ' ', None):
                data = {
                    'cad_x': coords[0],
                    'cad_y': coords[1],
                    'text': text
                    }
                tdata.append(data)

        return pd.DataFrame(tdata)

    def load_selections(self):
        bounders = self.msp.query('*[layer=="bounder"]')
        selections = list()

        for b in bounders:
            points = b.get_points()
            group = list()
            
            for p in points:
                coords = list(p)[:2]
                group.append(coords)
            
            selections.append(group)
        
        return selections
