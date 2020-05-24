import socket

from messaging.threads.IncomingMessagesThread import IncomingMessagesThread
from messaging.threads.PublishMessagesThread import PublishingMessagesThread
from messaging.messages.Message import Message

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
    def publish_message(self, message: Message):
        self.message_publisher.add_to_queue(message)

    # gestisco l'arrivo di u nuovo messaggio
    def handle_message(self, message: Message):
        # chiamo tutti i listener passando il nuovo messaggio raw
        for listener in self.listeners:
            listener(message)
