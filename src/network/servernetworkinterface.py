#!/usr/bin/env python3.6

import src.network.common
from src.network.message import Message, MessageType
from src.network.singleton import Singleton
from socket import *
from uuid import uuid4

class ServerNetworkInterface(metaclass=Singleton):

    """
    Sends and receives messages from the ClientNetworkInterface
    and various subsystems
    """

    # Class scoped variable for number of expected player connections
    MIN_PLAYERS = 6
    BUFSIZE = 4096
    PORT = 80

    def __init__(self):
        # '' is a symbolic representation for all interfaces
        self.address = ('', self.PORT)
        self.server_socket = None

        # UUID of server
        self._uuid = str(uuid4())

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
        # After 5 unsuccessful attempts to connect, reject that host
        self.server_socket.listen(5)

        # Wait until the minimum amount of players has connected
        # Synchronous
        while len(self.client_socket_list) != ServerNetworkInterface.MIN_PLAYERS:
            # Accept a connection
            client_sock, client_addr = self.server_socket.accept()
            client_uuid = str(uuid4())
            client = (client_uuid, client_sock)

            # Send UUID to client (perhaps use a Message later)
            uuid_msg = Message(self.get_uuid(), MessageType.GIVE_UUID, client_uuid)
            client[1].sendall(uuid_msg.serialize().encode())

            # Add connection to the CSL
            self.client_socket_list.append(client)
            print(f'Client from {client_addr} connected')
            print(f'DEBUG: {self.client_socket_list[-1]}')
        print('All players have connected successfully!')
    """ Getter for socket object associated with a specific uuid """
    def _get_sock_by_uuid(self, uuid):
        for conn in self.client_socket_list:
            if conn[0] == uuid:
                return conn[1]
        raise KeyError(f"Unable to find UUID: {uuid} in client list")

    """ Getter for the server's UUID """
    def get_uuid(self):
        return self._uuid

    """ Getter for count of currently connected players """
    def get_connection_count(self):
        return len(self.client_socket_list)

    """ Send message to a GameSocket """
    def send_message(self, uuid, message):
        # Need to get the socket object associated with a particular UUID
        client_sock = self._get_sock_by_uuid(uuid)
        # Verify that the UUID field is correct in our outgoing message
        if message.get_uuid() != self.get_uuid():
            message.set_uuid(self.get_uuid())
            print('DEBUG: Outgoing UUID had to be corrected!')
        try:
            client_sock.sendall(message.serialize().encode())
        except socket.timeout as e:
            print(f'Error: send_message timed out')
            return False
        return True

    """ Read message from a GameSocket """
    def read_message(self, uuid):
        # Grab the appropriate socket
        client_sock = self._get_sock_by_uuid(uuid)
        # Attempt to read a message
        try:
            message_string = client_sock.recv(self.BUFSIZE).decode()
        except socket.timeout as e:
            print(f'Error: read_message timed out')
            return None
        return Message.deserialize(message_string)

        """ Send message to all GameSocket """
    def send_all(self, message):
        status = True
        for conn in self.client_socket_list:
            if not self.send_message(conn[0], message):
                status = False
        return status

    """ Terminate all player connections """
    def close_all(self):
        # TODO: send all clients message that server is shutting down
        for conn in self.client_socket_list:
            conn[1].close()
            self.client_socket_list.remove(conn)

    """ Terminate all connections """
    def shutdown(self):
        print('DEBUG: Server is shutting down')
        self.close_all()
        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None
        exit(0)


if __name__ == '__main__':
    try:
        s = ServerNetworkInterface()
    except KeyboardInterrupt:
        print('Interrupted')
        exit(0)
