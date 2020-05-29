from typing import Callable, List

from environment.Tile import Tile
from utils.SupportClasses import TwoDPoint


class Sensor(object):
    fill = "red"

    def __init__(self, callback: Callable, vertexes: List[int], position: TwoDPoint, name: str, uncertainty: float = None):
        self._get_candidates: Callable = callback
        self._candidates: List[Tile] = []
        self.vertexes: List[int] = vertexes
        self.pose_vertexes: List[int] = vertexes
        self._sensor_position: TwoDPoint = position
        self.sensor_result = None
        self.name: str = name
        self._uncertainty: float = uncertainty

    def step(self):
        raise NotImplementedError

    def get_sensor_msg(self):
        raise NotImplementedError
