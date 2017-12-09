#!/usr/bin/env python3.6

from queue import Queue, Empty
import src.network.common
from src.network.message import Message, MessageType
from src.network.singleton import Singleton
from socket import *
from threading import Thread

class ClientNetworkInterface(metaclass=Singleton):

    """ Class scoped variable """
    # Maximum amount of bytes to read per message
    BUFSIZE = 4096
    # ServerNetworkInterface port
    PORT = 8080

    """ Constructor """
    def __init__(self):
        # Socket representing connection to a ServerNetworkInterface
        self._client_socket = None
        # UUID to be set on connect
        self._uuid = None
        # Queue that holds Messages from the Server
        self._msg_queue = Queue()

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
            self._client_socket = create_connection((ip, self.PORT), 5)
        except ConnectionError as e:
            print(f'Error: Failed to connect to ({ip},{self.PORT}).')
            print(f'Exception is {e}.')
            return False

        # Attempt to read the server's UUID assignment
        try:
            uuid_msg_string = self._client_socket.recv(self.BUFSIZE).decode()
            print(uuid_msg_string)
            uuid_msg = Message.deserialize(uuid_msg_string)
            if uuid_msg.get_msg_type() != MessageType.GIVE_UUID:
                raise ValueError('Error: Expected GIVE_UUID message, got {uuid_msg.get_msg_type()}')
            self._uuid = uuid_msg.get_payload()
            print(f'Successfully connected to server and assigned UUID:{self._uuid}')
        except OSError as e:
            print(f'Error: Failed to receive UUID message from server before timeout')
            return False

        t = Thread(target=self.listen, args=(self._msg_queue,), daemon=True)
        t.start()
        return True

    """ read thread's target function  """
    def listen(self, queue):
        while True:
            # Blocking read from server
            message_list = self._read_message()

    """ Returns top Message on Queue, or None if queue was empty """
    def get_message(self):
        try:
            return self._msg_queue.get_nowait()
        except Empty:
            return None

    """ Returns whether we have a valid connection to the server """
    def is_connected(self):
        return self._client_socket is not None

    """ Disconnect from the ServerNetworkInterface """
    def disconnect(self):
        if self.is_connected():
            # Close the connection
            self._client_socket.close()
            # Zeroize our connection variable
            self._client_socket = None

    """ Send message to a GameSocket """
    def send_message(self, message):
        if not self.is_connected():
            raise ConnectionError('Not connected to a server')
        # Verify that the message was created with the correct UUID
        if message.get_uuid() != self.get_uuid():
            message.set_uuid(self.get_uuid())
            print('DEBUG: Outgoing UUID has to be corrected!')

        try:
            self._client_socket.sendall(f"{message.serialize()}\n".encode())
        except socket.timeout as e:
            print(f'Error: send_message timed out')
            return False
        print("SEND_MSG: ", message)
        return True

    """ Read message from a GameSocket """
    def _read_message(self):
        if not self.is_connected():
            raise ConnectionError('Not connected to a server')
        try:
            message_string = self._client_socket.recv(self.BUFSIZE).decode()
        except socket.timeout as e:
            print(f'Error: read_message timed out')
            return None
        msg_list = message_string.split('\n')
        for msg in msg_list:
            if msg != '':
                self._msg_queue.put_nowait(Message.deserialize(msg))
        return msg_list

if __name__ == '__main__':
    try:
        c = ClientNetworkInterface()
        c.connect('104.236.203.126')
    except KeyboardInterrupt:
        print('Interrupted')
        exit(0)
