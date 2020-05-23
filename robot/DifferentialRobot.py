import numpy as np

from robot.TwoDRobot import TwoDRobot
from utils import MatrixTr


class DifferentialRobot(TwoDRobot):

    def __init__(self, length: int, vertex: [] = None):
        TwoDRobot.__init__(self, vertex)

        # velocità lineare e angolare
        self.vel_left = 0  # per andare avanti o indietro
        self.vel_right = 0  # per girarsi a destra o sinistra

        self.length: int = length  # larghezza dell'asse

    def simulate_dt(self, dt: int):
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
