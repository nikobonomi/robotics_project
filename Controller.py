import time

import numpy as np

from messaging.MessagingClient import MessagingClient
from messaging.messages.ProximitySensorMessage import ProximitySensorMessage
from messaging.messages.TwoDPose import TwoDPose
from messaging.messages.Velocity import Velocity
from utils.ErrorComputing import ErrorComputing
from utils.PID import PID
from utils.RateKeeper import RateKeeper


class Controller:
    def __init__(self, freq):
        self.messaging = MessagingClient()
        self.messaging.add_listener(self.handle_server_message)
        self.counter = 1
        self.rate = RateKeeper(freq)  # il rate è in hz
        self.pose = TwoDPose()
        self.goal = TwoDPose()
        self.goal.x = 200
        self.goal.y = 20

        self.x_pid = PID(freq, 1)
        self.z_pid = PID(freq, 3, 0, 0.1)
        self.target_x = 100
        self.done = False

    def handle_server_message(self, message):
        # mi assicuro che sia il messaggio giusto
        if message.is_type(TwoDPose):
            self.pose = message
        if message.is_type(ProximitySensorMessage):
            if message.sensor_value > 0:
                print(message)

    def is_at_goal(self, goal, tolerance=10):
        distance_error = ErrorComputing.euclidean_distance(self.pose, goal)
        return distance_error < tolerance

    def step_to_point(self, goal):
        message = Velocity()

        distance_error = ErrorComputing.euclidean_distance(self.pose, goal)
        target_angle = ErrorComputing.steering_angle(self.pose, goal)
        angle_error = ErrorComputing.angle_difference(target_angle, self.pose.theta)

        x_vel = self.x_pid.compute(distance_error)
        x_vel = np.clip(x_vel, 0, 20)
        # Linear velocity in the x-axis.
        message.x = x_vel

        # Angular velocity in the z-axis.

        z_vel = self.z_pid.compute(angle_error)
        z_vel = np.clip(z_vel, -0.4, 0.4)  # It's always a tourtle....

        message.z = z_vel

        # Publishing our vel_msg
        self.messaging.publish_message(message)

    def step(self):
        if not self.done:
            self.step_to_point(self.goal)
            self.done = self.is_at_goal(self.goal)
        elif self.done:
            # se è a posto allora ferma tutto
            self.messaging.publish_message(Velocity())

        self.rate.wait_cycle()


controller = Controller(10)

# piccolo sleep per dare tempo al socket di aprirsi e avviare il tutto
time.sleep(1)

while True:
    controller.step()

# controllo funzionamento rate keeper
# rate = RateKeeper(1)
# for i in range(10):
#     print(str(i))
#     time.sleep(0.0 + i/10)
#     rate.wait_cycle()
