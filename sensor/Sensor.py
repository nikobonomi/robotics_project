from typing import Callable, List

from environment.Tile import Tile
from utils.SupportClasses import TwoDPoint


class Sensor(object):
    def __init__(self, callback: Callable, vertexes: List[int], position: TwoDPoint):
        self._get_candidates: Callable = callback
        self.vertexes: List[int] = vertexes
        self.pose_vertexes: List[int] = vertexes
        self._sensor_position: TwoDPoint = position
        self._was_found: bool = False

    def step(self):
        raise NotImplementedError
