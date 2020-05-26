import string
from typing import List

from environment.Tile import Tile


class ColoredTile(Tile):
    filling = '#000'

    def __init__(self, x: float, y: float, width: float, height: float, color: string):
        vertex: List[float] = [x, y, x, y + height, x + width, y + height, x + width, y]

        Tile.__init__(self, vertex)
        self.filling = color
