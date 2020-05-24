import threading
import pickle

HEADERSIZE = 10


class IncomingMessagesThread(threading.Thread):
    def __init__(self, socket, function_callback):
        threading.Thread.__init__(self)
        self.callback = function_callback
        self.socket = socket

    def run(self):
        while True:
            full_message = b''
            msg = b''
            is_new_message = True
            msg_len = 0

            while True:
                try:
                    msg = self.socket.recv(16)
                    break
                except ConnectionAbortedError:
                    pass

                if is_new_message:
                    msg_len = int(msg[:HEADERSIZE])
                    is_new_message = False

                full_message += msg

                if len(full_message)-HEADERSIZE == msg_len:
                    self.callback(pickle.loads(full_message[HEADERSIZE:]))

                    is_new_message = True
                    full_message = b''
