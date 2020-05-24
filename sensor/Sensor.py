from typing import Callable


class Sensor(object):
    def __init__(self, callback: Callable):
        self._get_value: Callable = callback

    def step(self):
        raise NotImplementedError
