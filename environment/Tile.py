from typing import List


class Tile(object):
    filling = ''
    outline = ''
    width = 0

    def __init__(self, vertexes: List[int]):
        self.vertexes: List[int] = vertexes
