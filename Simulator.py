from ClockManager import ClockManager

from Graphics import SreGui
from messaging.MessagingServer import MessagingServer
from robot.DifferentialRobot import DifferentialRobot
from robot.TurtleRobot import TurtleRobot
from utils.RateKeeper import RateKeeper

RATE = 20 #hz

class Simulator:
    def __init__(self):

        self.messaging = MessagingServer()
        # faccio la subscription agli update dei client
        self.messaging.subscribe(self.handle_client_message)

        # inizializzo un nuovo robot
        # self.robot = DifferentialRobot(1)
        # self.robot.vel_left = 10
        # self.robot.vel_right = 11
        self.robot = TurtleRobot()
        self.robot.vel_linear = 1
        self.robot.vel_angular = 1

        self.gui = SreGui()
        self.gui.new_robot(self.robot)

        # inizializzo il clock manager
        # self._clock = ClockManager(1, self._step)
        self.rate = RateKeeper(RATE)

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

    def run(self):
        while True:
            self.robot.simulate_dt(1/RATE)
            self.gui.step_gui()
            self.rate.wait_cycle()

    def _step(self):
        self.robot.simulate_dt(1)
        print("step")
        self.gui.step_gui()




