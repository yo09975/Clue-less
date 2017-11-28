#!/usr/bin/env python3.6

from sys import *
import threading
import uuid
from socket import *

from src.network.gamesocket import *

PORT = 1337

class Server():
    def __init__(self, address):
        self.address = address
        self.socklist = []

    def start(self):
        sock = socket.socket(AF_INET, SOCK_STREAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        sock.bind(self.address)
        sock.listen(1)

        # Accept incoming connections
        while True:
            client, addr = sock.accept()
            print('Got connection from', addr)
            self.socklist.append(GameSocket(client))
            t = threading.Thread(target=self.connection_handler,
                                 args=(self.socklist[-1],))
            t.start()

    def connection_handler(self, gamesocket):
        while True:
            data = gamesocket.read_message()
            if not data:
                break
            gamesocket.get_socket().sendall(b'Got:' + data)
        print('Connection from ' + str(gamesocket.get_uuid()) + ' closed')
        gamesocket.close()

if __name__ == '__main__':
    try:
        s = Server(('', PORT))
        s.start()
    except KeyboardInterrupt:
        print('Interrupted')
        exit(0)

