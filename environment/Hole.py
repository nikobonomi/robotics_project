from environment.Obstacle import Obstacle


class Hole(Obstacle):
    def __init__(self, identifier, x, y, width, height):
        vertex = [x, y, x + width, y + height]

        Obstacle.__init__(self, identifier, vertex)
