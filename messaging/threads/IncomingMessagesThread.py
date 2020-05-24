import threading
import pickle


class IncomingMessagesThread(threading.Thread):
    def __init__(self, socket, function_callback):
        threading.Thread.__init__(self)
        self.callback = function_callback
        self.socket = socket

    def run(self):
        while True:
            # leggo i primi 2 bytes che identificano la lunghezza del messaggio
            message_length_bytes = b''
            for i in range(2):
                message_length_bytes += self.socket.recv(1)
            message_length = int.from_bytes(message_length_bytes, byteorder='big')
            # leggo tutti gli altri e compongo il messaggio
            # print("new message of length: " + str(message_length))
            message_bytes = b''
            for i in range(message_length):
                message_bytes += self.socket.recv(1)
            # mando il messaggio agli ascoltatori
            self.callback(pickle.loads(message_bytes))
