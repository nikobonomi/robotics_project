import threading
import pickle

HEADERSIZE = 10


class IncomingMessagesThread(threading.Thread):
    def __init__(self, socket, function_callback):
        threading.Thread.__init__(self)
        self.callback = function_callback
        self.socket = socket

    def read_bytes(self):
        return self.socket.recv(2048)

    def run(self):
        temp_save = b''
        buffer = b''
        msg_len = 0
        is_new_message = True
        cursor = 0

        while True:
            #print(str(cursor) + " " + str(len(buffer)))
            # verifico se serve una lettura
            if cursor >= len(buffer):
                try:

                    # chiedo una nuova lettura
                    buffer = self.read_bytes()

                    # aggiungo i bit salvati in precedenza davanti ai nuovi
                    buffer = temp_save + buffer
                    temp_save = b''
                    cursor = 0
                except ConnectionAbortedError:
                    pass

            if is_new_message:
                # 2 è la lunghezza dell'header
                # controllo se la lista buffer contiene abbastanza bit per rappresentare un header
                if cursor + 2 <= len(buffer):
                    # prendo 2 byte dalla lista, da cursor a cursor+2
                    msg_len = int.from_bytes(buffer[cursor: cursor + 2], byteorder='big')
                    is_new_message = False
                    # incremento il mio cursore
                    cursor += 2
                else:
                    # salvo i bytes in una variabile temporanea e chiedo una nuova lettura
                    temp_save = buffer[cursor:]
                    # imposto il cursore alla fine
                    cursor = len(buffer)

            # ora controllo di avere tutti i bytes del mio messaggio
            if cursor + msg_len <= len(buffer):
                # estraggo i bytes che mi servono
                message = buffer[cursor: cursor + msg_len]
                # imposto il cursore di conseguenza
                cursor += msg_len
                is_new_message = True
                # mando il messaggio deserializzato
                self.callback(pickle.loads(message))
                # ricomincio
            else:
                # in questo caso non ho abbastanza bytes per un messaggio completo
                # salvo i rimanenti nella variabile temporanea e chiedo una nuova lettura
                temp_save = buffer[cursor:]
                # imposto il cursore alla fine
                cursor = len(buffer)
