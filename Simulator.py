from ClockManager import ClockManager


class Simulator:
    def __init__(self):
        self._position = 0
        self._speed = 1
        self._clock = ClockManager(1, self._step)

    def _step(self):
        self._position += self._speed
        self.print_position()

    def print_position(self):
        print("My position is %d" % self._position)
