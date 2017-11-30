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
