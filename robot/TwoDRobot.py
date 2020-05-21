# general class for any TwoDimensional Robot
class TwoDRobot(object):
    def __init__(self, position, extremities):
        self.position = position
        self.extremities = extremities

    def move(self, trans_matrix):
        raise NotImplementedError()
