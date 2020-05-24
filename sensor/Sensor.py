from typing import Callable, List


class Sensor(object):
    def __init__(self, callback: Callable, vertexes: List[int]):
        self._get_value: Callable = callback
        self.vertexes: List[int] = vertexes

    def step(self):
        raise NotImplementedError
