from environment.Obstacle import Obstacle


class PolygonWall(Obstacle):
    def __init__(self, identifier, vertexes):
        vertex = vertexes

        Obstacle.__init__(self, identifier, vertex)

    @classmethod
    def square_wall(cls, identifier, x, y, width, height):
        vertex = [x, y, x, y + height, x + width, y + height, x + width, y]

        return cls(identifier, vertex)
