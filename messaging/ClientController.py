from messaging.MessagingClient import MessagingClient
import easygui


# dichiaro la funzione da chiamare all'arrivo di un messaggio
def handle_new_message(message):
    # in questo caso mostra un piccolo alert con il messaggio
    easygui.msgbox(message, title="Message from server")


# inizializzo l'helper
messagingHelper = MessagingClient()
messagingHelper.add_listener(handle_new_message)

# mi metto in attesa di un messaggio in console, e lo inoltro al server
while True:
    console_input = input("insert text to send to server: ")
    messagingHelper.publish_message(console_input)



