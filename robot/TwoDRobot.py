# generic class for any TwoDimensional Robot
from typing import List

import numpy as np
import math


# estraggo la posa dalla matrice
from sensor.Sensor import Sensor


class TwoDCartesianPose(object):
    def __init__(self, pose):
        self.x = np.around(pose[0, 2], decimals=2)
        self.y = np.around(pose[1, 2], decimals=2)
        self.theta = np.around(-math.atan2(pose[0, 0], pose[1, 0]) + np.pi / 2, decimals=5)
        # solo per test! poi da togliere!!
        self.theta += np.pi/4


class TwoDRobot(object):
    def __init__(self, vertex: List[int] = None, sensors: List[Sensor] = []):
        # posa del robot
        self.pose = np.eye(3)

        if vertex is None:
            vertex = [-10, -10, 0, -10, 10, 0, 0, 10, -10, 10]

        self._vertex: List[int] = vertex
        self.sensors: List[Sensor] = sensors

    def get_robot_draw_points(self) -> []:
        return self._vertex

    def simulate_dt(self, dt: int):
        raise NotImplementedError()

    def get_cartesian_pose(self) -> TwoDCartesianPose:
        return TwoDCartesianPose(self.pose)
