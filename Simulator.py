from ClockManager import ClockManager
import numpy as np
import matplotlib.pyplot as plt

from messaging.MessagingServer import MessagingServer
from robot.DifferentialRobot import DifferentialRobot


class Simulator:
    def __init__(self):
        self.messaging = MessagingServer()
        # faccio la subscription agli update dei client
        self.messaging.subscribe(self.handle_client_message)

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

        # inizializzo il clock manager
        self._clock = ClockManager(1, self._step)

    def handle_client_message(self, message):
        # martellata paura, ma almeno provo a cambiare i parametri del robot
        # so che il tipo di messaggio è uno solo, quindi splitto per estrarre i valori
        # ho messo la velocità sinistra in X e quella destra in Y
        # esempio: MSG_VEL X=0.3 Y=0.4 T=0
        data = message.split(" ")
        vel_left = data[1].split("=")[1]
        vel_right = data[2].split("=")[1]
        self.robot.vel_left = float(vel_left)
        self.robot.vel_right = float(vel_right)
        print("new vels: " + str(vel_left) + " " + str(vel_right))

    def _step(self):
        self.robot.simulate_dt(1)

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

