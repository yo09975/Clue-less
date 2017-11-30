#!/usr/bin/env python3.6
from singleton import Singleton
import uuid
from socket import *

class ServerNetworkInterface(metaclass=Singleton):
    """
    Sends and receives messages from the ClientNetworkInterface
    and various subsystems
    """
    
    """ Class scoped variable for amount of expected socket connections (players) """
    MIN_PLAYERS = 6
    BUFSIZE = 4096

    def __init__(self, address):
        # Tuple of (IP, PORT)
        self.address = address
        self.server_socket = None

        # UUID of server
        self._uuid = str(uuid.uuid4())

        # List of currently connected clients
        # Each element is a tuple of ((str) uuid, socket)
        self.client_socket_list = []
    
    """ Binds and listens for the appropriate number of players to connect """
    def start(self):
        # Create a TCP socket
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        # Prevents wonkiness when stopping/starting the server too fast
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        # Binds the socket to the given address tuple (e.g. (localhost, 1337))
        self.server_socket.bind(self.address)
        # Allow server to accept connections. After 5 unsuccessful attempts to connect, reject that host
        self.server_socket.listen(5)

        
        # Wait until the minimum amount of players has connected
        # Synchronous
        while len(self.client_socket_list) != ServerNetworkInterface.MIN_PLAYERS:
            # Accept a connection
            client_sock, client_addr = self.server_socket.accept()
            client = (str(uuid.uuid4()), client_sock)

            # Send UUID to client (perhaps use a Message later)
            client[1].sendall(f'{client[0]}'.encode())

            # Add connection to the CSL
            self.client_socket_list.append((str(uuid.uuid4()), client_sock))
            print(f'Client from {client_addr} connected')
            print(f'DEBUG: {self.client_socket_list[-1]}')
        print('All players have connected successfully!')

        # Debug
        for conn in self.client_socket_list:
            conn[1].sendall(f'Your UUID is {conn[0]}'.encode())
            # Close connection
            conn[1].close()
        # Close the server's socket
        self.server_socket.close()

    """ Retrieve the appropriate socket object associated with a particular uuid """
    def _get_sock_by_uuid(self, uuid):
        for conn in self.client_socket_list:
            if conn[0] == uuid:
                return conn[1]
        raise KeyError(f"Unable to find UUID: {uuid} in client list")

    """ Getter for the server's UUID """
    def get_uuid(self):
        return self._uuid

    """ Send message to a GameSocket """
    def send_message(self, uuid, message):
        raise NotImplementedError
    """ Read message from a GameSocket """
    def read_message(self, uuid):
        raise NotImplementedError
    """ Send message to all GameSocket """
    def send_all(self, message):
        raise NotImplementedError

if __name__ == '__main__':
    try:
        s = ServerNetworkInterface(('', 1337))
        s.start()
    except KeyboardInterrupt:
        print('Interrupted')
        exit(0)
