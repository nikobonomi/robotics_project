import numpy as np

from robot.TwoDRobot import TwoDRobot
from utils import MatrixTr


class DifferentialRobot(TwoDRobot):

    def __init__(self, length):
        TwoDRobot.__init__(self)

        # velocità lineare e angolare
        self.vel_left = 0  # per andare avanti o indietro
        self.vel_right = 0  # per girarsi a destra o sinistra

        self.length = length  # larghezza dell'asse

    def simulate_dt(self, dt):
        # simula il movimento del robot per durate dt aggiornandone la posa

        # se le velocità delle due ruote sono uguali allora va dritto
        if np.isclose(self.vel_left, self.vel_right):
            transformation_matrix = MatrixTr.mk_tr((self.vel_left + self.vel_right) / 2 * dt, 0)  # note we translate along x ()
        else:
            # altrimenti calcola omega che è la velocità angolare
            omega = (self.vel_right - self.vel_left) / (2 * self.length)
            # e il raggio della rotazione + la distanza
            r = self.length * (self.vel_right + self.vel_left) / (self.vel_right - self.vel_left)

            transformation_matrix = MatrixTr.mk_tr(0, r) @ MatrixTr.mk_rot(omega * dt) @ MatrixTr.mk_tr(0, -r)

        # calcola la nuova posa del robot
        self.pose = self.pose @ transformation_matrix

    def get_robot_draw_points(self):
        # in questo punto l'origine sta a 0,0
        return [-10, -10, 0, -10, 10, 0, 0, 10, -10, 10]

    # # lo mette in posizione x e y con angolazione theta
    # # sfruttanto la matrice pose
    # def draw_robot(self, ax=None, alpha=0.5):
    #     """ Draw robot at f, with wheel distance from center l,
    #     on axis ax (if provided) or on plt.gca() otherwise.
    #     if l is None, no wheels are drawn"""
    #
    #     # f = self.mk_tr(self.x, self.y) @ self.mk_rot(self.theta)
    #     f = self.pose
    #
    #     if not ax:
    #         ax = plt.gca()
    #
    #     robot = ([[-1, 2, -1, -1],  # x
    #               [-1, 0, 1, -1]])  # y
    #     robot = np.array(robot)
    #     robot = np.vstack((
    #         robot * 0.1,  # scale by 0.1 units
    #         np.ones((1, robot.shape[1]))))
    #
    #     robot_t = f @ robot
    #
    #     wheel_l = np.array([
    #         [-0.05, 0.05],
    #         [self.length, self.length],
    #         [1, 1]
    #     ])
    #     wheel_r = wheel_l * np.array([[1, -1, 1]]).T
    #     wheel_lt = f @ wheel_l
    #     wheel_rt = f @ wheel_r
    #     ax.plot(robot_t[0, :], robot_t[1, :], 'k-', alpha=alpha)
    #     ax.plot(wheel_lt[0, :], wheel_lt[1, :], 'k-', alpha=alpha)
    #     ax.plot(wheel_rt[0, :], wheel_rt[1, :], 'k-', alpha=alpha)