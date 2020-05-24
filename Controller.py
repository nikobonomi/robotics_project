import time

import numpy as np

from messaging.MessagingClient import MessagingClient
from messaging.messages.TwoDPose import TwoDPose
from messaging.messages.Velocity import Velocity
from utils.PID import PID
from utils.RateKeeper import RateKeeper


class Controller:
    def __init__(self, freq):
        self.messaging = MessagingClient()
        self.messaging.add_listener(self.handle_server_message)
        self.counter = 1
        self.rate = RateKeeper(freq)  # il rate è in hz
        self.pose = TwoDPose()

        self.pid = PID(freq, 1)
        self.target_x = 100

    def handle_server_message(self, message):
        # mi assicuro che sia il messaggio giusto
        if message.is_type(TwoDPose):
            self.pose = message

    def step(self):
        distance_error = self.target_x - self.pose.x

        x_vel = self.pid.compute(distance_error)
        vel_msg = Velocity()
        vel_msg.x = np.clip(x_vel, -20, 20)
        self.messaging.publish_message(vel_msg)

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
