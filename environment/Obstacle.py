from environment.Tile import Tile


class Obstacle(Tile):
    def __init__(self, identifier, vertex):
        super().__init__()
        self.identifier = identifier
        self.vertex = vertex
