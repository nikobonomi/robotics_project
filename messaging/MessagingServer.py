import socket
import threading


class ClientThread(threading.Thread):
    def __init__(self, client_address, connection_socket):
        threading.Thread.__init__(self)
        self.socket = connection_socket
        print("New connection added: ", client_address)

    def run(self):
        print("Connection from : ", clientAddress)
        msg = ''
        while True:
            data = self.socket.recv(2048)
            msg = data.decode()
            if msg == 'bye':
                break
            print("from client", msg)
            self.socket.send(bytes(str(msg).upper(), 'UTF-8'))

        print("Client at ", clientAddress, " disconnected...")


LOCALHOST = "127.0.0.1"
PORT = 2020
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")
while True:
    server.listen(1)
    client_sock, clientAddress = server.accept()
    new_thread = ClientThread(clientAddress, client_sock)
    new_thread.start()
