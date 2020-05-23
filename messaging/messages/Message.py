from typing import Dict
import pickle


class Message(object):
    def __init__(self):
        self.values: Dict = {}
        self.serialized: bytes = b''

    def serialize(self):
        self.serialized = pickle.dumps(self.values)

    def deserialize(self):
        self.values = pickle.loads(self.serialized)

    def to_string(self):
        raise NotImplementedError
