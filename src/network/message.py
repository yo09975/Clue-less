from enum import Enum
import json

class MessageType(Enum):

    """Contains player's requested move"""
    MOVEMENT = 1

    """Contains player's suggestion"""
    SUGGESTION_MAKE = 2

    """Contains cards for requesting an opponent to disprove"""
    SUGGESTION_REQUEST = 3

    """Contains one card to disprove suggestion"""
    SUGGESTION_RESPONSE = 4

    """Notifies every player of the suggestion issued """
    SUGGESTION_NOTIFY = 5

    """ Used to notify every player if a suggestion could be disproved"""
    SUGGESTION_OUTCOME = 6

    """Contain's player's accusation"""
    ACCUSATION = 7

    """Notify's all player's if accusation was correct of not"""
    ACCUSATION_NOTIFY = 8

    """Acknowledgement message for networking services"""
    ACK = 9

    """Negative acknowledgement message for networking services"""
    NACK = 10

    """Contains a message for all players not used for state transitions"""
    NOTIFY = 11

    """Contains player's UUID to set connect"""
    GIVE_UUID = 12

    """Contains a character the player wishes to play as in game"""
    SELECT_PIECE = 13

    """Contains serialized Board to update all players' board GUIs"""
    UPDATE_BOARD = 14

    """Player wishes to end their turn"""
    END_TURN = 15

    """Player wishes to leave the game"""
    LEAVE_GAME = 16

    """A player wants the game to start"""
    START_GAME = 17

    """Syncs PlayerList both server and client"""
    SEND_PLAYERS = 18

    """Contains a player's Hand serialized so that can know the cards they
       were dealt"""
    PLAYER_HAND = 19

    """Tells next player to start turn"""
    YOUR_TURN = 20


class Message:
    """
    Stores information to be transmitted between a client and server
    """

    """ Constructor """
    def __init__(self, uuid, msg_type, payload):
        """ Unique identifier for the originator of the Message """
        self._uuid = str(uuid)
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
    def serialize(self):
        msg = {}
        msg['uuid'] = self._uuid
        msg['msg_type'] = self._msg_type.value
        msg['payload'] = self._payload
        return json.dumps(msg)

    """ Stringifys the Message """
    def __str__(self):
        return f'{self.get_uuid()},{self.get_msg_type().value},{self.get_payload()}'

    def deserialize(message):
        if not isinstance(message, str):
            raise ValueError('Method expects string type parameter \'message_string\'')
        msg_dict = json.loads(message)
        return Message(msg_dict['uuid'], MessageType(msg_dict['msg_type']), msg_dict['payload'])
