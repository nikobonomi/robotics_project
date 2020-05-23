class Sensor:
    __value: float = 0

    def __init__(self):
        pass

    def step(self):
        self.update()

    @property
    def value(self) -> float:
        return self.__value

    def update(self):
        pass
