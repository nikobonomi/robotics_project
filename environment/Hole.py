from environment.Obstacle import Obstacle


class Hole(Obstacle):
    filling = '#000'
    width = 0
    outline = '#f00'

    def __init__(self, identifier, x, y, width, height):
        vertex = [x, y, x, y + height, x + width, y + height, x + width, y]

        Obstacle.__init__(self, identifier, vertex)
