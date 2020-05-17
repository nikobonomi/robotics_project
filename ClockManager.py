from threading import Timer


class ClockManager:
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self._interval = interval
        self._function = function
        self.args = args
        self.kwargs = kwargs
        self._is_running = False
        self.start()

    def _run(self):
        self._is_running = False
        self.start()
        self._function(*self.args, **self.kwargs)

    def start(self):
        if not self._is_running:
            self._timer = Timer(self._interval, self._run)
            self._timer.start()
            self._is_running = True

    def stop(self):
        self._timer.cancel()
        self._is_running = False
