import uuid
import socket

class GameSocket:
    """
    Creates and maintains TCP connections between game server and client.
    """

    """ Constructor """
    def __init__(self, socket):
        self._uuid = uuid.uuid4()
        self._socket = socket

    """ Used to send messages
        @param message The Message to send
    """
    def send_message(self, message):
        raise NotImplementedError

    """ Used to read Messages from the socket """
    def read_message(self):
        return self._socket.recv(10000)

    """ Getter for uuid """
    def get_uuid(self):
        return self._uuid

    """ Getter for socket"""
    def get_socket(self):
        return self._socket

    def close(self):
        return self._socket.close()
