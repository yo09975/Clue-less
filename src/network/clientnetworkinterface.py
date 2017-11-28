from singleton import Singleton


class ClientNetworkInterface(metaclass=Singleton):
    __connection = None

    """ Connect to the ServerNetworkInterface """
    def connect(self, ip, port):
        raise NotImplementedError
    """ Disconnect from the ServerNetworkInterface """
    def disconnect(self):
        raise NotImplementedError
    """ Send message to a GameSocket """
    def send_message(self, uuid, message):
        raise NotImplementedError
    """ Read message from a GameSocket """
    def read_message(self, uuid):
        raise NotImplementedError
    """ Send message to all GameSocket """
    def send_all(self, message):
        raise NotImplementedError
