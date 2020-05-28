import time

from client.ClosedLoopController import ClosedLoopController

from utils.RateKeeper import RateKeeper


class Controller:
    def __init__(self, freq):
        FREQ = 10

        self.rate_keeper = RateKeeper(10)

        # uso il controller in controller.py per far muovere il robottino
        self.controller = ClosedLoopController(FREQ)

        self.wall_ahead = False
        self.target_theta = 0

    def step(self):
        self.controller.step_straight(20)
        controller.rate_keeper.wait_cycle()


controller = Controller(10)

# piccolo sleep per dare tempo al socket di aprirsi e avviare il tutto
time.sleep(1)

while True:
    controller.step()
