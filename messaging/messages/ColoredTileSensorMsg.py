from messaging.messages.Message import Message


class ColoredTileSensorMsg(Message):
    def __init__(self, value: bool = False, name: str = "unknown", color: str = ""):
        super().__init__()
        self._message_type = ColoredTileSensorMsg
        self.sensor_value = value
        self.sensor_name = name
        self.sensor_color = color

    def __str__(self):
        return "MSG_PROXY N=%s V=%s C=%s" % (self.sensor_name, str(self.sensor_value), self.sensor_color)
