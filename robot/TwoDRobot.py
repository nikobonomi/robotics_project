# general class for any TwoDimensional Robot
import numpy as np
import math


class TwoDRobot(object):
    # def __init__(self, position, extremities):
    #     self.position = position
    #     self.extremities = extremities

    def __init__(self):
        # posa del robot
        self.pose = np.eye(3)
        self.gui_element = None

    def simulate_dt(self, dt):
        pass

    def get_cartesian_pose(self):
        # estraggo la posa dalla matrice
        x = self.pose[0, 2]
        y = self.pose[1, 2]
        theta = -math.atan2(self.pose[0, 0], self.pose[1, 0]) + np.pi/2
        return x, y, theta

    def get_robot_draw_points(self):
        pass

    # def move(self, trans_matrix):
    #     raise NotImplementedError()
