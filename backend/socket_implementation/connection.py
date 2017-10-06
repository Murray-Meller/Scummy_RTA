import socket
import time

class Connection(object):

        # Message length capped by buffer size
        # Communicating over TCP/IP and specifying a port

    def __init__(self, 
        target_address, target_port, 
        listener_address, listener_port, 
        buffer_size=1024):
        
        self.target_address = target_address
        self.target_port = target_port # Their port

        self.listener_address = listener_address
        self.listener_port = listener_port # Our port
        
        self.buffer_size = buffer_size
        self.listening = False
        self.bind()


    # Send a message
    def send(self, message):
        # Create our socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect to the target socket
        sock.connect((self.target_address, self.target_port))

        # Send our message and close the connection
        sock.send(bytes(message.encode()))
        print("Send: {message} to {port}".format(message=message, port=self.target_port))
        sock.close() 

    def bind(self):
        self.listening = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Bind our socket
        bound = False
        while not bound:
            try:
                self.listening.bind((self.listener_address, self.listener_port))
                bound=True
            except:
                print("Waiting for port:{port}...".format(port=self.listener_port))
                time.sleep(2)

    # Listen for a message
    def listen(self):

        if not self.listening:
        	self.bind()

        self.listening.listen(1)
        print("Listening on {address}:{port}...".format(address=self.listener_address, port=self.listener_port))

        # Get the connection and the address
        connection, address = self.listening.accept()

        # Get data up to the buffer size
        data = connection.recv(self.buffer_size)
        if not data: # No useful data printed
            return None
        else:
            print("{addr}:{data}".format(addr=address, data=data))
        connection.close()
        return data

# Handle message syntax
def syntax_handler(message, delimiter = '::', 
    comment = '##', command_split = ';;'):
    # Strip bytes formatting
    message = str(message)[2:-1]

    # Parse multiple commands
    commands = message.split(command_split)

    # Strip comments
    for command in commands:
        command = command.split(comment)[0]
   
    message_type = []
    message_data = []

    # Extract data fields
    for command in commands:
        message_type = command.split(delimiter)[0]
        message_data = message.split(delimiter)[1:]

    return message_type, message_data
