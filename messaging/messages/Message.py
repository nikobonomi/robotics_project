class Message(object):
    def __init__(self):
        self._message_type = None

    def is_type(self, cls):
        return self._message_type == cls

    def __str__(self):
        raise NotImplementedError
