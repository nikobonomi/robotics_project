from sensor.Sensor import Sensor
from environment.Tile import Tile
from typing import Callable, List, Type


class ProximitySensor(Sensor):
    def __init__(self, target: Type, callback: Callable, vertexes: List[int]):
        Sensor.__init__(self, callback, vertexes)
        self._target: Type = target
        self._value: List[Tile] = []
        self.range: float = -1

    def step(self):
        self._value = self._get_value()
        self.range: float = -1
        for i, tile in self._value:
            if isinstance(tile, self._target):
                self.range = i
                break
