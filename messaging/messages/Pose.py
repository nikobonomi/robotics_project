from messaging.messages.Message import Message


class Pose(Message):
    def __init__(self):
        super().__init__()

    def to_string(self):
        return "MSG_POSE X=" + str(self.values['x']) + " Y=" + str(self.values['y']) + " T=" + str(self.values['theta'])
