"""hand.py."""
from src.card import Card
import json

class Hand(object):
    """Represents a collection of Card objects

    Hand class in the Game Management Subsystem. The object containing
    all cards that make up a Player's hand at the start of a game.

    Attributes:
    _cards - List of Card objects

    """

    def __init__(self, cards: list):
        """Constructor"""
        # print('Constructor in Hand class')
        self._cards = cards

    def __str__(self) -> str:
        """Overridden toString method"""
        string = ''
        for card in self._cards:
            string += str(card.get_name()) + ', '
        return string[:-2]

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        return False

    def add_card(self, card: Card):
        """Accepts a Card object and adds it to the List of Cards"""
        # print('add_card method in Hand class')
        self._cards.append(card)

    def contains_card(self, card: Card) -> bool:
        """Accepts a Card object and returns a Boolean on whether the
        Card exists in the Hand"""
        # print('contains_card method in Hand class')
        return (card in self._cards)

    def get_cards(self):
        """Returns the entire List of Cards"""
        # print('get_cards method in Hand class')
        return self._cards

    def serialize(self):
        hand = {}
        for c in self._cards:
            hand[c.get_id()] = c.serialize()
        return json.dumps(hand)

    def deserialize(payload):
        hand_dict = json.loads(payload)
        hand = Hand([])
        for card_id in hand_dict:
            card = Card.deserialize(hand_dict[card_id])
            hand.add_card(card)
        return hand
