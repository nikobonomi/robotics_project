
from Graphics import SreGui
from messaging.MessagingServer import MessagingServer
from messaging.messages.TwoDPose import TwoDPose
from messaging.messages.Velocity import Velocity
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
        self.robot.enable_laser_sensor()
        self.gui = SreGui()
        self.gui.new_robot(self.robot)
        for sensor in self.robot.sensors_vertex:
            self.gui.new_sensor(self.robot, sensor)

        # inizializzo il clock manager
        # self._clock = ClockManager(1, self._step)
        self.rate = RateKeeper(RATE)

    def handle_client_message(self, message):
        #print(message)
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
            self.robot.simulate_dt(1/RATE)
            self.gui.step_gui()
            self.publish_pose()
            self.rate.wait_cycle()

    def _step(self):
        self.robot.simulate_dt(1)
        print("step")
        self.gui.step_gui()




