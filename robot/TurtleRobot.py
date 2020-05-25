import matplotlib.pyplot as plt
import numpy as np

# questo non va bene, da rivedere
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

    # lo mette in posizione x e y con angolazione theta
    # sfruttanto la matrice pose
    def draw_robot(self, ax=None, alpha=0.5):
        """ Draw robot at f, with wheel distance from center l,
        on axis ax (if provided) or on plt.gca() otherwise.
        if l is None, no wheels are drawn"""

        # f = self.mk_tr(self.x, self.y) @ self.mk_rot(self.theta)
        f = self.pose

        if not ax:
            ax = plt.gca()

        robot = ([[-1, 2, -1, -1],  # x
                  [-1, 0, 1, -1]])  # y
        robot = np.array(robot)
        robot = np.vstack((
            robot * 0.1,  # scale by 0.1 units
            np.ones((1, robot.shape[1]))))

        robot_t = f @ robot

        wheel_l = np.array([
            [-0.05, 0.05],
            [self.length, self.length],
            [1, 1]
        ])
        wheel_r = wheel_l * np.array([[1, -1, 1]]).T
        wheel_lt = f @ wheel_l
        wheel_rt = f @ wheel_r
        ax.plot(robot_t[0, :], robot_t[1, :], 'k-', alpha=alpha)
        ax.plot(wheel_lt[0, :], wheel_lt[1, :], 'k-', alpha=alpha)
        ax.plot(wheel_rt[0, :], wheel_rt[1, :], 'k-', alpha=alpha)
