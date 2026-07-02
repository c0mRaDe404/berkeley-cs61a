class Email:

    def __init__(self, msg, sender_name, recipient_name):
        self.msg = msg 
        self.sender_name = sender_name
        self.recipient_name = recipient_name 





class Server:

    def __init__(self):
        self.clients = {}

    def send(self, email): 
        recipient = self.clients[email.recipient_name]
        recipient.receive(email)

    def register_client(self, client, client_name):
        self.clients[client_name] = client 


class Client:

    def __init__(self, server, name):
        self.inbox = []
        self.name = name 
        self.server = server 
        server.register_client(self, name)
    def compose(self, msg, recipient_name):
        server.send(Email(msg, self.name, recipient_name))
    def receive(self, email):
        self.inbox.append(email)

