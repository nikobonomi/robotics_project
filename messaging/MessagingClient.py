import socket
import threading

SERVER = "127.0.0.1"
PORT = 2020


class MessagingClient:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((SERVER, PORT))
        # questa è una lista di callbacks, in modo che quando arriva un messaggio notifico tutti
        self.listeners = []

        # ci sono 2 threads, uno per mandare messaggi con la sua coda e uno che ascolta i nuovi messaggi
        # in questo modo non si mette in attesa il thread principale
        self.message_publisher = PublishingMessagesThread(self.client)
        self.message_listener = IncomingMessagesThread(self.client, self.handle_message)
        self.message_publisher.start()
        self.message_listener.start()

    def add_listener(self, function):
        self.listeners.append(function)

    # publico un messaggio al server
    def publish_message(self, message):
        self.message_publisher.add_to_queue(message)

    # gestisco l'arrivo di u nuovo messaggio
    def handle_message(self, message):
        # chiamo tutti i listener passando il nuovo messaggio raw
        for listener in self.listeners:
            listener(message)


class IncomingMessagesThread(threading.Thread):
    def __init__(self, client, function_callback):
        threading.Thread.__init__(self)
        self.callback = function_callback
        self.client = client

    def run(self):
        while True:
            in_data = self.client.recv(1024)
            # se c'è un nuovo messaggio lo passo alla callback
            self.callback(in_data.decode())


class PublishingMessagesThread(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.messagesQueue = []
        self.client = client

    def add_to_queue(self, message):
        self.messagesQueue.append(message)

    def run(self):
        while True:
            # se c'è qualcosa in coda lo mando, se no skippo
            if len(self.messagesQueue) > 0:
                # estraggo il più vecchio messaggio in coda (FIFO)
                self.client.sendall(bytes(self.messagesQueue.pop(0), 'UTF-8'))
