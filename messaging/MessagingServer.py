import socket
import threading

from messaging.threads.IncomingMessagesThread import IncomingMessagesThread
from messaging.threads.PublishMessagesThread import PublishingMessagesThread

LOCALHOST = "127.0.0.1"
PORT = 2020


class MessagingServer:
    def __init__(self):
        # nel costruttore tira già su il tutto
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((LOCALHOST, PORT))
        print("Server started")
        self.connection_watcher = ClientConnectionWatcher(server,self.handle_new_client)
        self.connection_watcher.start()

        self.connected_clients = []

    def handle_new_client(self, client_thread):
        self.connected_clients.append(client_thread)


# thread che aspetta la connessione di un nuovo client
class ClientConnectionWatcher(threading.Thread):

    def __init__(self, server, new_client_callback):
        threading.Thread.__init__(self)
        self.server = server
        self.new_client_callback = new_client_callback

    def run(self):
        print("Waiting for client request..")
        while True:
            self.server.listen(1)
            # rimango in attesa di una connessione
            client_sock, client_address = self.server.accept()
            # creo un handler per il client
            new_handler = ClientHandler(client_address, client_sock)
            # passo l'istanza alla callback
            self.new_client_callback(new_handler)
            # mi rimetto in ascolto di una nuova connessione


# questo handler rappresenta un client connesso
class ClientHandler:
    def __init__(self, client_address, connection_socket):
        self.socket = connection_socket
        # questa è una lista di callbacks, in modo che quando arriva un messaggio notifico tutti gli interessati
        # il listener è semplicemente una funzione che accetta una stringa come parametro
        self.listeners = []

        # ci sono 2 threads, uno per mandare messaggi con la sua coda e uno che ascolta i nuovi messaggi
        # in questo modo non si mette in attesa il thread principale
        self.message_publisher = PublishingMessagesThread(self.socket)
        self.message_listener = IncomingMessagesThread(self.socket, self.handle_message)
        self.message_publisher.start()
        self.message_listener.start()

    def add_listener(self, function):
        self.listeners.append(function)

    # publico un messaggio al client
    def publish_message(self, message):
        self.message_publisher.add_to_queue(message)

    # gestisco l'arrivo di un nuovo messaggio
    def handle_message(self, message):
        # chiamo tutti i listener passando il nuovo messaggio raw
        for listener in self.listeners:
            listener(message)




