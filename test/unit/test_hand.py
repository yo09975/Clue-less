"""test_hand.py"""
from src.card import Card
from src.cardtype import CardType
from src.hand import Hand


test_card1 = Card('Miss Scarlet', CardType.SUSPECT)
test_card2 = Card('Colonel Mustard', CardType.SUSPECT)
test_card3 = Card('Mrs. White', CardType.SUSPECT)
test_card4 = Card('Mr. Green', CardType.SUSPECT)
test_hand = Hand([test_card1, test_card2])

def test_init():
    assert type(test_hand) is Hand

def test_serialize():
    hand_serial = test_hand.serialize()
    assert hand_serial.find(f'"Miss Scarlet": "{test_card1.serialize()}", "Colonel Mustard": "{test_card2.serialize()}"')
def test_deserialize():
    hand_serial = test_hand.serialize()
    hand_deserial = Hand.deserialize(hand_serial)
    assert type(hand_deserial) is Hand
    assert hand_deserial == test_hand

def test_str():
    assert str(test_hand) == 'Miss Scarlet, Colonel Mustard'

def test_add_card():
    assert len(test_hand.get_cards()) == 2
    test_hand.add_card(test_card3)
    assert len(test_hand.get_cards()) == 3
    assert str(test_hand) == (
        'Miss Scarlet, Colonel Mustard, Mrs. White')

def test_contains_card():
    assert test_hand.contains_card(test_card2)
    assert not test_hand.contains_card(test_card4)


def test_get_cards():
    for list_card in test_hand.get_cards():
        assert test_hand.contains_card(list_card)
