from typing import List
from environment.Tile import Tile


class Obstacle(Tile):
    outline = '#000'
    width = 3

    def __init__(self, identifier, vertexes: List[int]):
        super().__init__(vertexes)
        self.identifier = identifier
