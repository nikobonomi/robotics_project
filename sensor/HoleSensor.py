from environment.Hole import Hole
from sensor.Sensor import Sensor
from environment.Tile import Tile
from typing import Callable, List, Type

from utils.SupportClasses import TwoDPoint


class HoleSensor(Sensor):
    def __init__(self, callback: Callable, position: TwoDPoint, name: str):
        vertexes = [0, 0, 5, 5, -5, -5]
        Sensor.__init__(self, callback, vertexes, position, name)
        self._target: Type = Hole

    def step(self):
        self._candidates: List[Tile] = self._get_candidates(self)
        self.was_found: bool = False

        for tile in self._candidates:
            if isinstance(tile, self._target):
                self.was_found: bool = True
                return
