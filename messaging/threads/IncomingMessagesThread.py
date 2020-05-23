import threading

from messaging.messages.Message import Message


class IncomingMessagesThread(threading.Thread):
    def __init__(self, socket, function_callback):
        threading.Thread.__init__(self)
        self.callback = function_callback
        self.socket = socket

    def run(self):
        while True:
            in_data = self.socket.recv(1024)
            # se c'è un nuovo messaggio lo passo alla callback
            self.callback(Message.deserialize(in_data))
