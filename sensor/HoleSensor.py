from environment.Hole import Hole
from sensor.Sensor import Sensor
from environment.Tile import Tile
from typing import Callable, List, Type

from utils.SupportClasses import TwoDPoint


class HoleSensor(Sensor):
    def __init__(self, callback: Callable, position: TwoDPoint, name: str):
        vertexes = [0, 0, 20, 20, -20, -20]
        Sensor.__init__(self, callback, vertexes, position, name)
        self._target: Type = Hole
        self.sensor_result: bool = False

    def step(self):
        self._candidates: List[Tile] = self._get_candidates(self)
        self.sensor_result: bool = False

        for tile in self._candidates:
            if isinstance(tile, self._target):
                self.sensor_result: bool = True
                return
