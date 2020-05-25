from sensor.Sensor import Sensor
from environment.Tile import Tile
from typing import Callable, List, Type


class ProximitySensor(Sensor):
    def __init__(self, target: Type, callback: Callable, vertexes: List[int], x: int = 0, y: int = 0):
        Sensor.__init__(self, callback, vertexes)
        self._target: Type = target
        self._value: List[Tile] = []
        self.range: float = -1
        self._x = x
        self._y = y

    def step(self):
        self._value: List[Tile] = self._get_value()
        self.range: float = -1
        for tile in self._value:
            if isinstance(tile, self._target):
                # get tile distance from sensor
                self.range = self._target_distance(tile)
                break

    def _target_distance(self, target: Tile) -> float:
        # todo calcolare distanza tra il sensore e l'oggetto
        x = target.vertexes[1] - self._x
        return 3.3
