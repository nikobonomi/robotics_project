from typing import Callable, List

from environment.Tile import Tile


class Sensor(object):
    def __init__(self, callback: Callable, vertexes: List[int]):
        self._get_value: Callable = callback
        self.vertexes: List[int] = vertexes
        self.pose_vertexes: List[int] = vertexes

    def step(self, candidates: List[Tile]):
        raise NotImplementedError
