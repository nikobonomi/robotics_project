from sensor.Sensor import Sensor
from environment.Tile import Tile
from typing import Callable, List, Type


class ProximitySensor(Sensor):
    def __init__(self, max_range: int, target: Type, callback: Callable):
        Sensor.__init__(self, callback)
        self._target: Type = target
        self._value: List[Tile] = []
        self.max_range: int = max_range
        self.range = -1

    def step(self):
        self._value = self._get_value()
        self.range = -1
        for i, tile in self._value:
            if isinstance(tile, self._target):
                self.range = i
                break
