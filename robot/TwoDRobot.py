# generic class for any TwoDimensional Robot
import numpy as np
import math


# estraggo la posa dalla matrice
class TwoDCartesianPose(object):
    def __init__(self, pose):
        self.x = pose[0, 2]
        self.y = pose[1, 2]
        self.theta = -math.atan2(pose[0, 0], pose[1, 0]) + np.pi / 2


class TwoDRobot(object):
    def __init__(self, vertex: [] = None):
        # posa del robot
        self.pose = np.eye(3)

        if vertex is None:
            vertex = [-10, -10, 0, -10, 10, 0, 0, 10, -10, 10]

        self._vertex = vertex

    def get_robot_draw_points(self) -> []:
        return self._vertex

    def simulate_dt(self, dt: int):
        raise NotImplementedError()

    def get_cartesian_pose(self) -> TwoDCartesianPose:
        return TwoDCartesianPose(self.pose)
