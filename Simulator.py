from ClockManager import ClockManager
import numpy as np
import matplotlib.pyplot as plt

from messaging.MessagingServer import MessagingServer



class Simulator:
    def __init__(self):
        self._position = 0
        self._speed = 1
        self._clock = ClockManager(1, self._step)
        self.messaging = MessagingServer()
        self.draw_frame(np.eye(3))  # disegno il frame di riferimento

    def _step(self):
        self._position += self._speed
        self.print_position()

    def print_position(self):
        print("My position is %d" % self._position)

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

