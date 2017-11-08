from hand import Hand
from random import shuffle
from card import Card


class Deck(Hand):
    """Represents a collection of Card objects. Extends the Hand class.

    Deck class in the Game Management Subsystem. This class is a subclass
    of the Hand class.
    """

    def __init__(self, cards: list):
        """Constructor"""
        # print('Constructor in Deck class')
        super(Deck, self).__init__(cards)

    def __add__(self, deck: Hand):
        """Overrides the addition operation. Creates a new Deck from
        combining the parameter and reference Decks"""
        # print('__add__ method in Deck class')
        return Deck(self._cards + deck._cards)

    def shuffle(self):
        """Randomizes the order of the Cards in the Deck"""
        # print('shuffle method in Deck class')
        shuffle(self._cards)

    def deal(self) -> Card:
        """Returns the top card in the Deck"""
        # print('deal method in Deck class')
        return self._cards.pop()
