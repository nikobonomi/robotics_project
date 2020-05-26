from environment.ColoredTile import ColoredTile
from sensor.Sensor import Sensor
from environment.Tile import Tile
from typing import Callable, List, Type

from utils.SupportClasses import TwoDPoint


class ColoredTileSensor(Sensor):
    def __init__(self, callback: Callable, position: TwoDPoint, name: str, color: str = None):
        vertexes = [0, 0, 5, 5, -5, -5]
        Sensor.__init__(self, callback, vertexes, position, name)
        self._target: Type = ColoredTile
        self._color: str = color

    def step(self):
        self._candidates: List[Tile] = self._get_candidates(self)
        self.was_found: bool = False

        for tile in self._candidates:
            if isinstance(tile, self._target) and (tile.filling == self._color or self._color is None):
                self.was_found: bool = True
                return
