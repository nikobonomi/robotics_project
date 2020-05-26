import time

from Graphics import SreGui
from environment.Hole import Hole
from environment.Obstacle import Obstacle
from environment.PolygonWall import PolygonWall
from environment.SquareWall import SquareWall
from messaging.MessagingServer import MessagingServer
from messaging.messages.ProximitySensorMsg import ProximitySensorMsg
from messaging.messages.VelocityMsg import VelocityMsg
from robot.TurtleRobot import TurtleRobot
from sensor.ProximitySensor import ProximitySensor
from utils.RateKeeper import RateKeeper
from utils.SupportClasses import TwoDPoint

RATE = 20  # hz


class Simulator:
    def __init__(self):

        self.messaging = MessagingServer()
        # faccio la subscription agli update dei client
        self.messaging.subscribe(self.handle_client_message)

        self.gui = SreGui()

        # inizializzo un nuovo robot
        # self.robot = DifferentialRobot(1)
        # self.robot.vel_left = 10
        # self.robot.vel_right = 11
        self.robot = TurtleRobot()
        temp_sensor = ProximitySensor(Obstacle, self.gui.sensor_callback, [10, 0, 30, 0], TwoDPoint(10, 0), "f_c")
        self.robot.sensors.append(temp_sensor)
        temp_sensor = ProximitySensor(Obstacle, self.gui.sensor_callback, [5, -10, 28, -14], TwoDPoint(10, -10), "f_r")
        self.robot.sensors.append(temp_sensor)
        temp_sensor = ProximitySensor(Obstacle, self.gui.sensor_callback, [5, 10, 28, 14], TwoDPoint(10, 10), "f_l")
        self.robot.sensors.append(temp_sensor)
        temp_sensor = ProximitySensor(Obstacle, self.gui.sensor_callback, [-15, 8, -25, 8], TwoDPoint(-15, 8), "b_r")
        self.robot.sensors.append(temp_sensor)
        temp_sensor = ProximitySensor(Obstacle, self.gui.sensor_callback, [-15, -8, -25, -8], TwoDPoint(-15, -8), "b_l")
        self.robot.sensors.append(temp_sensor)
        temp_obstacle = PolygonWall("obstacle 1", [50, 88, 162, -68, 311, -67, 196, 103, 216, 2])
        temp_obstacle2 = SquareWall("obstacle 2", 100, 110, 20, 20)
        temp_obstacle3 = SquareWall("obstacle 3", -100, 100, 20, 20)
        temp_hole = Hole("ciao", -200, -200, 30, 30)
        self.gui.new_robot(self.robot)
        self.gui.new_tile(temp_obstacle)
        self.gui.new_tile(temp_obstacle2)
        self.gui.new_tile(temp_obstacle3)
        self.gui.new_tile(temp_hole)

        # inizializzo il clock manager
        # self._clock = ClockManager(1, self._step)
        self.rate = RateKeeper(RATE)

    def handle_client_message(self, message):
        # print(message)
        # per il momento c'è solo 1 robot... il tartaruga
        # quindi mi assicuro di ricevere un messaggio che sia adatto a quel robot
        if message.is_type(VelocityMsg):
            self.robot.vel_linear = message.x
            self.robot.vel_angular = message.z

    def publish_messages(self):
        for message in self.robot.get_status_messages():
            self.messaging.publish_to_all(message)

    def run(self):
        while True:
            self.robot.simulate_dt(1 / RATE)
            self.gui.step_gui()
            # deve essere fatto dopo l'update della gui
            # perchè usa il motore grafico per calcolare i valori dei sensori
            self.robot.simulate_sensors()
            self.publish_messages()
            self.rate.wait_cycle()

    def _step(self):
        self.robot.simulate_dt(1)
        self.gui.step_gui()
