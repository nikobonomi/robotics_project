from typing import List

import numpy as np

# questo non va bene, da rivedere
from messaging.messages.Message import Message
from messaging.messages.ProximitySensorMsg import ProximitySensorMsg
from messaging.messages.TwoDPoseMsg import TwoDPoseMsg
from robot.TwoDRobot import TwoDRobot


class TurtleRobot(TwoDRobot):

    def __init__(self):
        TwoDRobot.__init__(self,
                           [
                               0, 15,
                               5, 15,
                               5, 5,
                               10, 5,
                               10, -5,
                               5, -5,
                               5, -15,
                               0, -15,
                               0, -11,
                               -15, -11,
                               -15, -5,
                               -10, -5,
                               -10, 5,
                               -15, 5,
                               -15, 11,
                               0, 11
                           ]
                           )
        self.pose = np.eye(3)

        # velocità lineare e angolare
        self.vel_linear = 0  # per andare avanti o indietro
        self.vel_angular = 0  # per girarsi a destra o sinistra

    def simulate_dt(self, dt: float):
        # if we are moving straight, R is at the infinity and we handle this case separately
        if self.vel_angular == 0:
            transformation_matrix = self.mk_tr(self.vel_linear * dt, 0)
        else:
            # # altrimenti calcola omega che è la velocità angolare
            # omega = (self.vel_right - self.vel_left) / (2 * self.length)
            # # e il raggio della rotazione + la distanza
            r = 10 * self.vel_linear
            #
            # transformation_matrix = MatrixTr.mk_tr(0, r) @ MatrixTr.mk_rot(omega * dt) @ MatrixTr.mk_tr(0, -r)

            transformation_matrix = self.mk_tr(self.vel_linear * dt, 0) @ self.mk_rot(self.vel_angular * dt)

        self.pose = self.pose @ transformation_matrix

    def simulate_sensors(self):
        for s in self.sensors:
            s.step()

    @staticmethod
    def mk_tr(x, y):
        return np.array([[1, 0, x],
                         [0, 1, y],
                         [0, 0, 1]])

    @staticmethod
    def mk_rot(theta):
        return np.array([[np.cos(theta), -np.sin(theta), 0],
                         [np.sin(theta), np.cos(theta), 0],
                         [0, 0, 1]])

    def get_status_messages(self) -> List[Message]:
        results: List[Message] = []

        cartesian_pose = self.get_cartesian_pose()
        # messaggio di posa del robot
        pose_message = TwoDPoseMsg()
        pose_message.x = cartesian_pose.x
        pose_message.y = cartesian_pose.y
        pose_message.theta = cartesian_pose.theta

        results.append(pose_message)

        # ora guardo per ogni sensore
        for sensor in self.sensors:
            results.append(sensor.get_sensor_msg())

        return results
