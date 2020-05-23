from messaging.messages.Message import Message


class Velocity(Message):
    def __init__(self):
        super().__init__()
        self.linear = 0
        self.angular = 0

    def to_string(self):
        return "MSG_VEL LIN=" + str(self.linear) + " ANG=" + str(self.angular)


