from enum import Enum


class MessageType(Enum):
    MOVEMENT = 1
    SUGGESTION_MAKE = 2
    SUGGESTION_REQUEST = 3
    SUGGESTION_RESPONSE = 4
    SUGGESTION_NOTIFY = 5
    ACCUSATION = 6
    ACCUSATION_NOTIFY = 7
    ACK = 8
    NACK = 9
    NOTIFY = 10
    GIVE_UUID = 11
    SELECT_PIECE = 12
    UPDATE_BOARD = 13
    END_TURN = 14
    LEAVE_GAME = 15
    START_GAME = 16
    SEND_PLAYERS = 17

class Message:
    """
    Stores information to be transmitted between a client and server
    """

    """ Constructor """
    def __init__(self, uuid, msg_type, payload):
        """ Unique identifier for the originator of the Message """
        self._uuid = uuid
        """ msg_type must be in the MessageType enum """
        if isinstance(msg_type, MessageType):
            self._msg_type = msg_type
        else:
            raise ValueError
        """ payload is a string containing the actual data """
        self._payload = payload

    """ Setter for uuid """
    def set_uuid(self, uuid):
        self._uuid = uuid

    """ Getter for uuid """
    def get_uuid(self):
        return self._uuid

    """ Getter for msg_type """
    def get_msg_type(self):
        return self._msg_type

    """ Getter for payload """
    def get_payload(self):
        return self._payload

    """ Stringifys and returns a byte representation of a Message """
    def encode(self):
        return str(self).encode()

    """ Stringifys the Message """
    def __str__(self):
        return f'{self.get_uuid()},{self.get_msg_type().value},{self.get_payload()}'
