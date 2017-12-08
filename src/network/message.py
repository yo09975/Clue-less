from enum import Enum


class MessageType(Enum):

    MOVEMENT = 1
    """Contains player's requested move"""
    SUGGESTION_MAKE = 2
    """Contains player's suggestion"""
    SUGGESTION_REQUEST = 3
    """Contains cards for requesting an opponent to disprove"""
    SUGGESTION_RESPONSE = 4
    """Contains one card to disprove suggestion"""
    SUGGESTION_NOTIFY = 5
    """Notifies every player whether suggestion was disproved or not"""
    ACCUSATION = 6
    """Contain's player's accusation"""
    ACCUSATION_NOTIFY = 7
    """Notify's all player's if accusation was correct of not"""
    ACK = 8
    """Acknowledgement message for networking services"""
    NACK = 9
    """Negative acknowledgement message for networking services"""
    NOTIFY = 10
    """Contains a message for all players"""
    GIVE_UUID = 11
    """Contains player's UUID to set connect"""
    SELECT_PIECE = 12
    """Contains a character the player wishes to play as in game"""
    UPDATE_BOARD = 13
    """Contains serialized Board to update all players' board GUIs"""
    END_TURN = 14
    """Player wishes to end their turn"""
    LEAVE_GAME = 15
    """Player wishes to leave the game"""
    START_GAME = 16
    """A player wants the game to start"""
    SEND_PLAYERS = 17
    """Syncs PlayerList both server and client"""
    PLAYER_HAND = 18
    """Contains a player's Hand serialized so that can know the cards they
       were dealt"""
    YOUR_TURN = 19
    """Tells next player to start turn"""


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
