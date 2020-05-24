from messaging.messages.Message import Message


class Velocity(Message):
    def __init__(self):
        super().__init__()
        self.wheel_right = 0
        self.wheel_left = 0

    def to_string(self):
        return "MSG_VEL RIGHT=" + str(self.wheel_right) + " LEFT=" + str(self.wheel_left)

