from typing import Dict
import pickle


class Message(object):

    def serialize(self):
        return pickle.dumps(self)

    @staticmethod
    def deserialize(data: bytes):
        message = Message
        message.values = pickle.loads(data)

    def to_string(self):
        raise NotImplementedError
