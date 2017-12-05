"""card.py."""
from src.cardtype import CardType


class Card(object):
    """Represents a weapon, room, or suspect card.

    Card class in the Game Management Subsystem. Each object is a
    representation of a suspect, room, or weapon in the game.

    _name - String that is the name of the Card
    _card_type - Enum representing the type of Card (Suspect, Room, or Weapon)
    _card_id - String representing an unique Card ID

    """

    def __init__(self, name: str, card_type: CardType, card_id: str):
        """Constructor"""
        # print('Constructor in Card class')
        self._name = name
        self._card_type = card_type
        self._card_id = card_id

    def __str__(self) -> str:
        """Overridden toString method"""
        card_string = str(self._name) + ' '
        card_string += str(self._card_type) + ' '
        card_string += str(self._card_id)
        return card_string

    def get_name(self) -> str:
        """Returns a String with the name of the Card"""
        # print('get_name method in Card class')
        return self._name

    def get_id(self) -> str:
        """Returns a String with the ID of the Card"""
        # print('get_id method in Card class')
        return self._card_id

    def get_type(self) -> CardType:
        """Returns an Enum that represents the type of the Card"""
        # print('get_type method in Card class')
        return self._card_type

    def serialize(self, payload):
        """serialize card_id to a JSON file"""
        card = {}
        card['card_id'] = self.get_id()
        return json.dumps(payload)

