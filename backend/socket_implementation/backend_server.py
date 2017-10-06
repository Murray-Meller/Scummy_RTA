import socket
from connection import Connection, syntax_handler
import time
import numpy as np

# -----------------------------------------------------------------------------------
# This option is somewhat harder than the api one, but is included if you are
# interested in building what is effectively your own TCP/IP webserver from 
# just about scratch
# -----------------------------------------------------------------------------------

host_addr = "localhost"
server_port = 8080 # Hosts the web server
frontend_port = 8081 # For communicating with the front end
backend_port = 8082 # For communicating with the back end

delimiter = "::"

# -----------------------------------------------------------------------------------
# Our fake database

users = {}

# -----------------------------------------------------------------------------------

# Backend inherits from the Connection class
class Backend(object):
    
    def __init__(self, 
        target_address, target_port, 
        listener_address, listener_port, 
        delimiter = '::', running=True):
        
        self.handler = {}
        self.delimiter = delimiter
        self.running = running
        self.connection = Connection(target_address, target_port, listener_address, listener_port)

    def get_request(self):

        raw_message = self.connection.listen()
        response_type, response_data = syntax_handler(raw_message, delimiter=self.delimiter)

        # Decide what to do with the message
        response = self.handle_request(response_type, response_data)

        # Handle multiple response types
        if response is not None:
            try:
                time.sleep(0.3)
                self.connection.send(response)
            except:
                self.connection.send(response[0])

    # Handle a request
    def handle_request(self, response_type, response_data):
        return self.handler[response_type](*response_data)

    # Handle a new type of message
    def handler_add(self, message_type, message_handler):
        self.handler[message_type] = message_handler

    def format_response(self, response_type, contents):
        return "{response_type}{delimiter}{response_contents}".format(
            delimiter=self.delimiter, response_type=response_type, response_contents=contents)

# -----------------------------------------------------------------------------------
# Let's build our own handlers to take the parsed commands and use them

# USERADD
def handle_useradd(username, password, *args):
    print(username, password)
    if username in users:
        return backend.format_response("STR", "Username already exists")
    users[username] = password
    return backend.format_response("BOOL", "True")

# LOGIN
def handle_login(username, password, *args):
    if username in users:
        if users[username] == password:
            return backend.format_response("BOOL", "True")
    return backend.format_response("BOOL", "False")

# SHUTDOWN
def handle_shutdown(message_data, *args):
    backend.running = False
    return None

# -----------------------------------------------------------------------------------

backend = Backend(host_addr, frontend_port, host_addr, backend_port)

backend.handler_add("USERADD", handle_useradd)
backend.handler_add("LOGIN", handle_login)
backend.handler_add("SHUTDOWN", handle_shutdown)

# -----------------------------------------------------------------------------------

while backend.running:
    backend.get_request()

