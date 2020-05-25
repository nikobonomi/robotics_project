from sensor.Sensor import Sensor
from environment.Tile import Tile
from typing import Callable, List, Type

from utils.SpacialCalculations import line_intersection, distance


class ProximitySensor(Sensor):
    def __init__(self, target: Type, callback: Callable, vertexes: List[int], x: int = 0, y: int = 0):
        Sensor.__init__(self, callback, vertexes)
        self._target: Type = target
        self._value: List[Tile] = []
        self.range: float = -1
        self._x = x
        self._y = y

    def step(self, candidates: List[Tile]):
        # self._value: List[Tile] = self._get_value()
        self.range: float = -1
        for tile in candidates:
            if isinstance(tile, self._target):
                # get tile distance from sensor
                self.range = self._target_distance(tile)

    def _target_distance(self, target: Tile) -> float:
        # cerco su tutti i lati del poligono del tile se c'è un'intersezione

        line_start = self.pose_vertexes[0], self.pose_vertexes[1]
        line_end = self.pose_vertexes[2], self.pose_vertexes[3]

        for cursor in range(0, len(target.vertexes), 2):
            # prendo i vertici attuali
            edge_start = target.vertexes[cursor], target.vertexes[cursor+1]
            # se sono all'ultimo vertice allora prendo i primi della lista
            if cursor+3 > len(target.vertexes):
                edge_end = target.vertexes[0], target.vertexes[1]
            else:
                edge_end = target.vertexes[cursor + 2], target.vertexes[cursor + 3]

            # ora cerco una possibile intersezione
            intersection = line_intersection((line_start, line_end), (edge_start, edge_end))

            # se intersection è none vuol dire che non ci sono, ma se è true allora c'è qualcosa
            if intersection is not None:
                x, y = intersection
                dist = distance((line_start, intersection))
                print("intersezione a distanza " + str(dist) + " al punto " + str(x) + "," + str(y) )





        # todo calcolare distanza tra il sensore e l'oggetto
        x = target.vertexes[1] - self._x
        return 3.3
