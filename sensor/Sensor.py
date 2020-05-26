from typing import Callable, List

from environment.Tile import Tile
from utils.SupportClasses import TwoDPoint


class Sensor(object):
    def __init__(self, callback: Callable, vertexes: List[int], position: TwoDPoint, name):
        self._get_candidates: Callable = callback
        self.vertexes: List[int] = vertexes
        self.pose_vertexes: List[int] = vertexes
        self._sensor_position: TwoDPoint = position
        self._was_found: bool = False
        self.name = name
        self.sensor_result: float = -1  # rappresenta la distanza dal tile più vicino

    def step(self):
        raise NotImplementedError
