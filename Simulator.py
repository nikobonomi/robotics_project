from Graphics import SreGui
from environment.Obstacle import Obstacle
from messaging.MessagingServer import MessagingServer
from messaging.messages.TwoDPose import TwoDPose
from messaging.messages.Velocity import Velocity
from robot.TurtleRobot import TurtleRobot
from sensor.ProximitySensor import ProximitySensor
from utils.RateKeeper import RateKeeper

RATE = 20  # hz


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
        temp_sensor = ProximitySensor(Obstacle, self.temp, [10, -1, 30, -1, 30, 1, 10, 1])
        self.robot.sensors.append(temp_sensor)
        temp_sensor = ProximitySensor(Obstacle, self.temp, [-15, 8, -25, 8, -25, 6, -15, 6])
        self.robot.sensors.append(temp_sensor)
        temp_sensor = ProximitySensor(Obstacle, self.temp, [-15, -9, -25, -9, -25, -7, -15, -7])
        self.robot.sensors.append(temp_sensor)
        self.gui = SreGui()
        self.gui.new_robot(self.robot)

        # inizializzo il clock manager
        # self._clock = ClockManager(1, self._step)
        self.rate = RateKeeper(RATE)

    def temp(self):
        pass

    def handle_client_message(self, message):
        # print(message)
        # per il momento c'è solo 1 robot... il tartaruga
        # quindi mi assicuro di ricevere un messaggio che sia adatto a quel robot
        if message.is_type(Velocity):
            self.robot.vel_linear = message.x
            self.robot.vel_angular = message.theta

    def publish_pose(self):
        pose = TwoDPose()
        pose.x = self.robot.get_cartesian_pose().x
        pose.y = self.robot.get_cartesian_pose().y
        pose.theta = self.robot.get_cartesian_pose().theta
        self.messaging.publish_to_all(pose)

    def run(self):
        while True:
            self.robot.simulate_dt(1 / RATE)
            self.gui.step_gui()
            self.publish_pose()
            self.rate.wait_cycle()

    def _step(self):
        self.robot.simulate_dt(1)
        print("step")
        self.gui.step_gui()
