import time
from random import randrange

from ClockManager import ClockManager
from messaging.MessagingClient import MessagingClient
from messaging.MessagingServer import MessagingServer
from messaging.messages.Pose import Pose


def send_message():
    msg = Pose()
    msg.x = 10
    msg.y = randrange(5,15)
    server.publish_to_all(msg)


def print_message(msg: Pose):
    print(str(msg))


server = MessagingServer()
time.sleep(1)
client = MessagingClient()
client.add_listener(print_message)
clock = ClockManager(1, send_message)
