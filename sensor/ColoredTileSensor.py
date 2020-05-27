from environment.ColoredTile import ColoredTile
from sensor.Sensor import Sensor
from environment.Tile import Tile
from typing import Callable, List, Type

from utils.SupportClasses import TwoDPoint


class ColoredTileSensor(Sensor):
    fill = 'yellow'

    def __init__(self, callback: Callable, position: TwoDPoint, name: str, color: str = None):
        vertexes = [-15, 0, 15, 0]
        Sensor.__init__(self, callback, vertexes, position, name)
        self._target: Type = ColoredTile
        self._color: str = color
        self.sensor_result: bool = False

    def step(self):
        self._candidates: List[Tile] = self._get_candidates(self)
        self.sensor_result: bool = False

        for tile in self._candidates:
            if isinstance(tile, self._target) and (tile.filling == self._color or self._color is None):
                self.sensor_result: bool = True
                return
