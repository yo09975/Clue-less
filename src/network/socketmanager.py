class SocketManager:
    """
    Singleton that keeps track of player connections
    """
    """ Constructor """
    def __init__(self):
        _player_connections = []
        return

    """ Getter for instance of singleton """
    def get_instance(self):
        raise NotImplementedError

    """ Getter for connection list """
    def get_connections(self):
        return self._player_connections

    """ Adds connections to the list """
    def add_connection(self, connection):
        raise NotImplementedError

    """ Removes connections from the list """
    def remove_connection(self, connection):
        raise NotImplementedError
