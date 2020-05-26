from messaging.messages.Message import Message


class ProximitySensorMsg(Message):
    def __init__(self):
        super().__init__()
        self._message_type = ProximitySensorMsg
        self.sensor_value = -1
        self.sensor_name = "unknown"

    def __str__(self):
        return "MSG_PROXY N=" + self.sensor_name + " D=" + str(self.sensor_value)
