from messaging.messages.Message import Message


class VelocityMsg(Message):
    def __init__(self):
        super().__init__()
        self._message_type = VelocityMsg
        self.x = 0
        self.y = 0
        self.z = 0

    def __str__(self):
        return "MSG_VEL X=" + str(self.x) + " Y=" + str(self.y) + " Z=" + str(self.z)
