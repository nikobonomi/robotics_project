from typing import List
from environment.Tile import Tile


class Obstacle(Tile):
    def __init__(self, identifier, vertexes: List[int]):
        super().__init__(vertexes)
        self.identifier = identifier
