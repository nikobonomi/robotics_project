from random import random

from environment.ColoredTile import ColoredTile
from messaging.messages.ColoredTileSensorMsg import ColoredTileSensorMsg
from sensor.Sensor import Sensor
from environment.Tile import Tile
from typing import Callable, List, Type

from utils.SupportClasses import TwoDPoint


class ColoredTileSensor(Sensor):
    fill = 'yellow'

    def __init__(self, callback: Callable, position: TwoDPoint, name: str, color: str = None, uncertainty: float = None):
        vertexes = [-15, 0, 15, 0]
        super().__init__(callback, vertexes, position, name, uncertainty)
        self._target: Type = ColoredTile
        self._color: str = color
        self._detected_color: str = ""
        self.sensor_result: bool = False

    def step(self):
        self._candidates: List[Tile] = self._get_candidates(self)
        self.sensor_result: bool = False
        self._detected_color: str = ""

        for tile in self._candidates:
            if isinstance(tile, self._target) and (tile.filling == self._color or self._color is None):
                self.sensor_result: bool = True
                self._detected_color: str = tile.filling

        if self._uncertainty is not None:
            if random.randrange(100) < self._uncertainty * 100:
                self.sensor_result = not self.sensor_result

    def get_sensor_msg(self) -> ColoredTileSensorMsg:
        return ColoredTileSensorMsg(self.sensor_result, self.name, self._detected_color)
