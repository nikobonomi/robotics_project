from environment.Hole import Hole
from messaging.messages.HoleSensorMsg import HoleSensorMsg
from sensor.Sensor import Sensor
from environment.Tile import Tile
from typing import Callable, List, Type

from utils.SupportClasses import TwoDPoint


class HoleSensor(Sensor):
    fill = 'lime'

    def __init__(self, callback: Callable, position: TwoDPoint, name: str):
        vertexes = [-15, 0, 25, 0]
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

    def get_sensor_msg(self) -> HoleSensorMsg:
        return HoleSensorMsg(self.sensor_result, self.name)
