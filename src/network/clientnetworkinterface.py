#!/usr/bin/env python3.6

from singleton import Singleton
from servernetworkinterface import *
from socket import *

class ClientNetworkInterface(metaclass=Singleton):
    
    """ Constructor """
    def __init__(self):
        # Socket representing connection to a ServerNetworkInterface
        self.client_socket = None

    """ Connect to the ServerNetworkInterface """
    def connect(self, ip):
        if self.is_connected():
            print('Already connected to server!')
            return True

        # Create a TCP socket connection to server
        try:
            self.client_socket = create_connection((ip, ServerNetworkInterface.PORT), 5)
        except Exception as e:
            print(f'Error: Failed to connect to ({ip},{ServerNetworkInterface.PORT}). Exception is {e}.')
            return False
    
    """ Returns whether we have a valid connection to the server """
    def is_connected(self):
        return self.client_socket != None

    """ Disconnect from the ServerNetworkInterface """
    def disconnect(self):
        if self.is_connected():
            # Close the connection
            self.client_socket.close()
            # Zeroize our connection variable
            self.client_socket = None

    """ Send message to a GameSocket """
    def send_message(self, uuid, message):
        raise NotImplementedError

    """ Read message from a GameSocket """
    def read_message(self, uuid):
        raise NotImplementedError

if __name__ == '__main__':
    try:
        c = ClientNetworkInterface()
        c.connect('localhost')
        c2 = ClientNetworkInterface()
        c2.connect('localhost')
    except KeyboardInterrupt:
        print('Interrupted')
        exit(0)

