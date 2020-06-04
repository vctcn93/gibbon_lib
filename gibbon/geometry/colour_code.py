import numpy as np


class ColourCode:
    def __init__(self, colours=[[196, 86, 90], [255, 196, 0], [0, 154, 255]], domain=[0, 1]):
        self._colours = [np.array(c) for c in colours]
        self.domain = domain
        self.normalized = [c / 255 for c in self._colours]

    @property
    def colours(self):
        return [c.tolist() for c in self._colours]

    @staticmethod
    def divide_by_quantity(quantity: int):
        ls = list(range(int(quantity)))
        new = [0] * quantity

        for i in range(quantity):
            new[i] = ls[i] / (quantity - 1)

        return new

    def colour_by_param(self, param: float):
        if param < self.domain[0]:
            param = self.domain[0]

        elif param > self.domain[1]:
            param = self.domain[1]

        position = (len(self.colours) - 1) * (param / (self.domain[1] - self.domain[0]))
        index = int(np.floor(position))

        if index >= len(self.colours)-1:
            return self.colours[-1]

        c1, c2 = self.normalized[index], self.normalized[index + 1]
        t = position % 1
        result = c1.copy()
        result += (c2 - c1) * t
        result *= 255
        result = result.astype(int)
        return result.tolist()

    def colours_by_quantity(self, quantity: int):
        params = self.divide_by_quantity(quantity)
        return [self.colour_by_param(param) for param in params]


if __name__ == '__main__':
    c = ColourCode()
    assert c.colour_by_param(.3) == [231, 152, 36]
    assert c.colours_by_quantity(8) == [
        [196, 86, 90],
        [212, 117, 64],
        [229, 148, 38],
        [246, 180, 12],
        [218, 190, 36],
        [145, 178, 109],
        [72, 166, 182],
        [0, 154, 255]
    ]
