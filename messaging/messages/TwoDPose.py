from messaging.messages.Message import Message


class TwoDPose(Message):
    def __init__(self):
        super().__init__()
        self._message_type = TwoDPose
        self.x = 0
        self.y = 0
        self.theta = 0

    def __str__(self):
        return "MSG_POSE X=" + str(self.x) + " Y=" + str(self.y) + " T=" + str(self.theta)
