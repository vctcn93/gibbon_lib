from cell import Cell


class FiniteCell(Cell):
    def __init__(self, coords: list, size: float):
        super().__init__(coords, size)
        self._scores = dict()
        self._forbidden = dict()

    @property
    def scores(self) -> dict:
        return self._scores

    @property
    def score(self) -> float:
        return sum(
            [sum(scores) for scores in self._scores.values()]
        ) if self.status else 0

    @property
    def status(self) -> bool:
        return all([len(fb) == 0 for fb in self._forbidden.values()])

    @property
    def forbidden(self) -> list:
        return [key for key, value in self._forbidden.items() if len(value) != 0]

    def subject_score(self, key) -> float:
        return sum(self._scores[key])


if __name__ == '__main__':
    c = FiniteCell([0, 0], 10)
    assert c.vertices == [[-5, -5], [5, -5], [5, 5], [-5, 5]]
    assert c.faces == [0, 1, 2, 3]
    assert c.colours == [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]]
    assert c.mesh == {
        'tp': 'mesh',
        'v': [[-5, -5], [5, -5], [5, 5], [-5, 5]],
        'f': [0, 1, 2, 3],
        'c': [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]]
    }
    c.set_colour([128, 128, 128])
    assert c.colours == [[128, 128, 128], [128, 128, 128], [128, 128, 128], [128, 128, 128]]
