"""card.py."""
from src.cardtype import CardType
import json

class Card(object):
    """Represents a weapon, room, or suspect card.

    Card class in the Game Management Subsystem. Each object is a
    representation of a suspect, room, or weapon in the game.

    _card_id - String representing an unique Card ID
    _card_type - Enum representing the type of Card (Suspect, Room, or Weapon)

    """

    def __init__(self, card_id: str, card_type: CardType):
        """Constructor"""
        # print('Constructor in Card class')
        self._card_type = card_type
        self._card_id = card_id

    def __str__(self) -> str:
        """Overridden toString method"""
        card_string = str(self._card_id) + ' '
        card_string += str(self._card_type)
        return card_string

    def __eq__(self, other):
        """ Overridden equality check """
        if isinstance(self, other.__class__):
                return self.__dict__ == other.__dict__
        return False

    def get_id(self) -> str:
        """Returns a String with the ID of the Card"""
        # print('get_id method in Card class')
        return self._card_id

    def get_type(self) -> CardType:
        """Returns an Enum that represents the type of the Card"""
        # print('get_type method in Card class')
        return self._card_type

    def serialize(self):
        card = {}
        card['card_id'] = self._card_id
        card['card_type'] = self._card_type.value
        return json.dumps(card)

    def deserialize(payload):
        card = json.loads(payload)
        return Card(card['card_id'], CardType(card['card_type']))
