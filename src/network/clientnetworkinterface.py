#!/usr/bin/env python3.6

from singleton import Singleton
from servernetworkinterface import *
from socket import *
from message import *

class ClientNetworkInterface(metaclass=Singleton):
    
    """ Constructor """
    def __init__(self):
        # Socket representing connection to a ServerNetworkInterface
        self._client_socket = None
        self._uuid = None

    """ Getter for uuid """
    def get_uuid(self):
        return self._uuid

    """ Connect to the ServerNetworkInterface """
    def connect(self, ip):
        if self.is_connected():
            print('Already connected to server!')
            return True
        
        # Create a TCP socket connection to server
        try:
            self._client_socket = create_connection((ip, ServerNetworkInterface.PORT), 5)
            self._uuid = self._client_socket.recv(ServerNetworkInterface.BUFSIZE).decode()
            print(f'Successfully connected to server and assigned UUID:{self._uuid}')
        except Exception as e:
            print(f'Error: Failed to connect to ({ip},{ServerNetworkInterface.PORT}). Exception is {e}.')
            return False
    
    """ Returns whether we have a valid connection to the server """
    def is_connected(self):
        return self._client_socket != None

    """ Disconnect from the ServerNetworkInterface """
    def disconnect(self):
        if self.is_connected():
            # Close the connection
            self._client_socket.close()
            # Zeroize our connection variable
            self._client_socket = None

    """ Send message to a GameSocket """
    def send_message(self, message):
        # Verify that the message was created with the correct UUID
        if message.get_uuid() != self.get_uuid():
            message.set_uuid(self.get_uuid())
            print('DEBUG: Outgoing UUID has to be corrected!')

        # TODO: Error checking/retry logic
        self._client_socket.sendall(message.encode())
        
    """ Read message from a GameSocket """
    def read_message(self, uuid):
        raise NotImplementedError

if __name__ == '__main__':
    try:
        c = ClientNetworkInterface()
        c.connect('localhost')
    except KeyboardInterrupt:
        print('Interrupted')
        exit(0)

