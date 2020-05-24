class Message(object):
    def __init__(self):
        self._message_type = None

    def _is(self, cls):
        return self._message_type == cls

    def to_string(self):
        raise NotImplementedError
