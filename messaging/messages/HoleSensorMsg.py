from messaging.messages.Message import Message


class HoleSensorMsg(Message):
    def __init__(self, value: bool = False, name: str = "unknown"):
        super().__init__()
        self._message_type = HoleSensorMsg
        self.sensor_value = value
        self.sensor_name = name

    def __str__(self):
        return "MSG_PROXY N=%s D=%s" % (self.sensor_name, str(self.sensor_value))
