from ClockManager import ClockManager
import numpy as np
import matplotlib.pyplot as plt

from messaging.MessagingServer import MessagingServer
from messaging.robot.DifferentialRobot import DifferentialRobot


class Simulator:
    def __init__(self):
        self._clock = ClockManager(2, self._step)
        self.messaging = MessagingServer()
        # inizializzo un nuovo robot
        self.robot = DifferentialRobot(0.1)
        self.robot.vel_left = 0.2
        self.robot.vel_right = 0.3
        fig = plt.figure()
        self.ax = fig.add_subplot()
        # stampo lo stato iniziale
        self.draw_frame(np.eye(3))  # disegno il frame di riferimento
        self.robot.draw_robot()
        plt.axis("equal")
        plt.show()

    def _step(self):
        self.robot.simulate_dt(2)

        self.draw_frame(np.eye(3))  # disegno il frame di riferimento
        self.robot.draw_robot()
        plt.axis("equal")
        plt.show()


    @staticmethod
    def draw_frame(f, ax=None, name=None):
        """ Draw frame defined by f on axis ax (if provided) or on plt.gca() otherwise """
        x_hat = f @ np.array([[0, 0, 1], [1, 0, 1]]).T
        y_hat = f @ np.array([[0, 0, 1], [0, 1, 1]]).T
        if not ax:
            ax = plt.gca()
        ax.plot(x_hat[0, :], x_hat[1, :], 'r-')  # transformed x unit vector
        ax.plot(y_hat[0, :], y_hat[1, :], 'g-')  # transformed y unit vector
        if name:
            ax.text(x_hat[0, 0], x_hat[1, 0], name, va="top", ha="center")

