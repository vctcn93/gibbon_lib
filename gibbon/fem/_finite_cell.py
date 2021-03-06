from gibbon.geometry import Cell


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
