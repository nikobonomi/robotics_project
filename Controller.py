from messaging.MessagingClient import MessagingClient
from messaging.messages.Velocity import Velocity
from messaging.utils.RateKeeper import RateKeeper
import time


class Controller:
    def __init__(self):
        self.messaging = MessagingClient()
        self.messaging.add_listener(self.handle_server_message)
        self.counter = 0
        self.rate = RateKeeper(2) # il rate è in hz

    def handle_server_message(self, message):
        print(message)

    def step(self):
        # quando il contatore arriva a 10 cambia la vel di una ruota
        if self.counter == 10:
            vel = Velocity()
            vel.x = 0.2
            vel.y = 0.2
            vel.theta = 0
            self.messaging.publish_message(vel.get_message_string())
            print("mando messaggio al server")
        elif self.counter == 20:
            vel = Velocity()
            vel.x = 0.3
            vel.y = 0.2
            vel.theta = 0
            self.messaging.publish_message(vel.get_message_string())
            print("mando messaggio al server")
        self.counter = self.counter + 1
        self.rate.wait_cycle()


controller = Controller()

while True:
    controller.step()

# controllo funzionamento rate keeper
# rate = RateKeeper(1)
# for i in range(10):
#     print(str(i))
#     time.sleep(0.0 + i/10)
#     rate.wait_cycle()
