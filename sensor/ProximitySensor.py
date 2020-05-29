from random import random

from messaging.messages.ProximitySensorMsg import ProximitySensorMsg
from sensor.Sensor import Sensor
from environment.Tile import Tile
from typing import Callable, List, Type

from utils.SpacialCalculations import line_intersection, distance
from utils.SupportClasses import TwoDPoint


class ProximitySensor(Sensor):
    def __init__(self, target: Type, callback: Callable, vertexes: List[int], position: TwoDPoint, name, uncertainty: float = None, systematic: float = None):
        super().__init__(callback, vertexes, position, name, uncertainty)
        self._target: Type = target
        self.sensor_result: float = -1  # rappresenta la distanza dal tile più vicino
        self._systematic: float = systematic

    def step(self):
        self._candidates: List[Tile] = self._get_candidates(self)
        self.sensor_result = 15
        if len(self._candidates) > 0:
            self.sensor_result = 9999
        for tile in self._candidates:
            if isinstance(tile, self._target):
                # get tile distance from sensor
                temp = self._target_distance(tile)
                if temp < self.sensor_result:
                    self.sensor_result = temp

        if self._uncertainty is not None:
            if random.randrange(100) < self._uncertainty*100:
                self.sensor_result = random.randrange(-100, 100)

        if self._systematic is not None:
            self.sensor_result = (self.sensor_result * (1 + self._systematic))

    def _target_distance(self, target: Tile) -> float:
        # cerco su tutti i lati del poligono del tile se c'è un'intersezione

        line_start = self.pose_vertexes[0], self.pose_vertexes[1]
        line_end = self.pose_vertexes[2], self.pose_vertexes[3]

        return_dist = 9999

        for cursor in range(0, len(target.vertexes), 2):
            # prendo i vertici attuali
            edge_start = target.vertexes[cursor], target.vertexes[cursor + 1]
            # se sono all'ultimo vertice allora prendo i primi della lista
            if cursor + 3 > len(target.vertexes):
                edge_end = target.vertexes[0], target.vertexes[1]
            else:
                edge_end = target.vertexes[cursor + 2], target.vertexes[cursor + 3]

            # ora cerco una possibile intersezione
            intersection = line_intersection((line_start, line_end), (edge_start, edge_end))

            # se intersection è none vuol dire che non ci sono, ma se è true allora c'è qualcosa
            if intersection is not None:
                x, y = intersection
                dist = distance((line_start, intersection))
                if return_dist > dist:
                    return_dist = dist
                # print("intersezione a distanza " + str(dist) + " al punto " + str(x) + "," + str(y))
        # print("intersezione a distanza " + str(return_dist))
        return return_dist

    def get_sensor_msg(self) -> ProximitySensorMsg:
        return ProximitySensorMsg(self.sensor_result, self.name)
