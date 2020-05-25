from typing import Tuple


class TwoDPoint(object):
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y

    def get_tuple(self) -> Tuple:
        return self.x, self.y
