import sys, os

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from src.network.servernetworkinterface import ServerNetworkInterface as SNI
from src.gamecontroller import GameController


print("gc")
gc = GameController()


sni = SNI()
sni.start()
while True:
    for c in sni.client_socket_list:
        usr = c[0]
        msg = sni.read_message(usr)
        if msg is not None:
            print("reading", msg)
            gc.read_message(msg)
