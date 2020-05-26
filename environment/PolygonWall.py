from environment.Obstacle import Obstacle


class PolygonWall(Obstacle):
    def __init__(self, identifier, vertexes):
        vertex = vertexes

        Obstacle.__init__(self, identifier, vertex)
