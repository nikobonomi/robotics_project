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
                # creo la lista di bytes
                message_bytes = pickle.dumps(self.messagesQueue.pop(0))
                # aggiungo davanti 2 bytes che identificano la lunghezza
                message_bytes = len(message_bytes).to_bytes(2, byteorder='big') + message_bytes
                # mando il messaggio
                self.socket.sendall(message_bytes)
