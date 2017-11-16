from singleton import Singleton


class ServerNetworkInterface(metaclass=Singleton):
    """
    Sends and receives messages from the ClientNetworkInterface
    and various subsystems
    """

    """ Send message to a GameSocket """
    def send_message(self, uuid, message):
        raise NotImplementedError
    """ Read message from a GameSocket """
    def read_message(self, uuid):
        raise NotImplementedError
    """ Send message to all GameSocket """
    def send_all(self, message):
        raise NotImplementedError
