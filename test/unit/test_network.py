import multiprocessing
import threading
import time
from src.network.clientnetworkinterface import ClientNetworkInterface
from src.network.servernetworkinterface import ServerNetworkInterface
from src.network.message import Message, MessageType

cni = ClientNetworkInterface()
sni = ServerNetworkInterface()

test_msg_type = MessageType.MOVEMENT
test_msg_payload = 'testing'

def test_start_server():
    newThread = threading.Thread(target=listen, args=())
    newThread.daemon = True
    newThread.start()
    assert True

def test_connect_to_server():
    assert cni.connect('0.0.0.0') == True
    assert cni.is_connected() == True
    assert sni.get_connection_count() == 1

def test_send_message_to_server():
    mess = Message(cni.get_uuid(), test_msg_type, test_msg_payload)
    assert cni.send_message(mess)


def test_read_message_from_client():
    client_uuid = sni.client_socket_list[0][0]
    message = sni.read_message(client_uuid)
    assert message is not None
    assert message.get_uuid() == client_uuid
    assert message.get_msg_type() == test_msg_type
    assert message.get_payload() == test_msg_payload

def test_send_message_to_client():
    server_uuid = sni.get_uuid()
    client_uuid = cni.get_uuid()
    mess = Message(server_uuid, test_msg_type, test_msg_payload)
    assert sni.send_message(client_uuid, mess) == True

def test_read_message_from_server():
    server_uuid = sni.get_uuid()
    client_uuid = cni.get_uuid()
    """ Logic to wait 5 seconds for message to come through """
    for i in range(1,6):
        mess = cni.get_message()
        if not mess:
            time.sleep(1)
        else:
            break
    assert mess is not None
    assert mess.get_uuid() == server_uuid
    assert mess.get_msg_type() == test_msg_type
    assert mess.get_payload() == test_msg_payload

def test_send_all():
    mess = Message(sni.get_uuid(), test_msg_type, test_msg_payload)
    multiprocessing.set_start_method('spawn')
    p = multiprocessing.Process(target=second_connection, args=())
    p.start()
    p.join()
    assert sni.get_connection_count() == 2
    assert sni.send_all(mess) == True
    #client_uuid = cni.get_uuid()
    #assert sni.send_message(client_uuid, mess) == True

    """ Logic to wait 5 seconds for message to come through """
    for i in range(1,6):
        recvd_msg = cni.get_message()
        if not recvd_msg:
            time.sleep(1)
        else:
            break

    assert recvd_msg is not None
    assert recvd_msg.get_uuid() == sni.get_uuid()
    assert recvd_msg.get_msg_type() == test_msg_type
    assert recvd_msg.get_payload() == test_msg_payload

def second_connection():
    cni2 = ClientNetworkInterface()
    cni2.connect('0.0.0.0')

def listen():
    sni.start()
