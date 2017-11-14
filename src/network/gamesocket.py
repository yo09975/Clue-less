import uuid


class GameSocket:
    """
    Creates and maintains TCP connections between game server and client.
    """

    """ Constructor """
    def __init__(self, uuid, connection):
        self._uuid = uuid
        self._connection = connection

    """ Used to send messages
        @param message The Message to send
    """
    def send_message(self, message):
        raise NotImplementedError

    """ Used to read Messages from the connection """
    def read_message(self):
        raise NotImplementedError

    """ Getter for uuid """
    def get_uuid(self):
        return self._uuid

    """ Getter for connection"""
    def get_connection(self):
        return self._connection
