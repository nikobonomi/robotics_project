import threading
import pickle

class PublishingMessagesThread(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.messagesQueue = []
        self.socket = socket

    def add_to_queue(self, message):
        self.messagesQueue.append(message)

    def run(self):
        while True:
            # se c'è qualcosa in coda lo mando, se no skippo
            if len(self.messagesQueue) > 0:
                # estraggo il più vecchio messaggio in coda (FIFO)
                self.socket.sendall(pickle.dumps(self.messagesQueue.pop(0)))
