import socket
import numpy as np
from connection import Connection, syntax_handler
from bottle import run, request, get, post 


# ----------------------------------------------------------------------------------

host_addr = "localhost"
server_port = 8080 # Hosts the server
frontend_port = 8081
backend_port = 8082

# ----------------------------------------------------------------------------------

class Frontend(object):
    
    def __init__(self, target_address, target_port, listener_address, listener_port, delimiter = '::'):
        self.handler = {}
        self.delimiter = delimiter
        self.vhandle_response = np.vectorize(self.handle_response) 
        self.connection = Connection(target_address, target_port, listener_address, listener_port)

    def __call__(self, message):
        self.send(message)

    def send(self, message):
        self.connection.send(message)

    def get_response(self):

        raw_message = self.connection.listen()

        response_type, response_data = syntax_handler(raw_message, delimiter=self.delimiter)

        # Decide what to do with the message
        #try:
        response = self.handle_response(response_type, response_data)
        print(response)
        return response
        #except:
        #    return None

    def handle_response(self, response_type, response_data):
        return self.handler[response_type](*response_data)

    # Handle a new type of message
    def handler_add(self, message_type, message_handler):
        self.handler[message_type] = message_handler

# ----------------------------------------------------------------------------------

# Check if a boolean response is "True"
def handle_bool(message_data):
    return message_data.lower() == 'true'

# Return the string 
def handle_string(message_data):
    return message_data

# Parse to int
def handle_int(message_data):
    return int(message_data)

# ----------------------------------------------------------------------------------

@get('/')
def showuser():
    return '''
        Login with a username and password
        <form action="/" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>
    '''

def call_useradd(username, password):
    backend_call = "USERADD{delimiter}{username}{delimiter}{password}".format(
        username=username, password=password, delimiter=frontend.delimiter)
    frontend(backend_call)

@post('/')
def useradd():
    username = request.forms.get("username")
    password = request.forms.get("password")
    
    # Call the backend connection
    call_useradd(username, password)
    
    # Get the response
    response = frontend.get_response()
    
    if response is True:
        return 'User created successfully!'
    else:
        return response

# ----------------------------------------------------------------------------------

frontend = Frontend(host_addr, backend_port, host_addr, frontend_port)

frontend.handler_add("BOOL", handle_bool)
frontend.handler_add("INT", handle_int)
frontend.handler_add("STR", handle_string)

# ----------------------------------------------------------------------------------

run(host=host_addr, port=server_port)