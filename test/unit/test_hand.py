"""test_hand.py"""
from src.card import Card
from src.cardtype import CardType
from src.hand import Hand


test_card1 = Card('Test Card 1 Name', CardType.SUSPECT, 'TEST111ID')
test_card2 = Card('Test Card 2 Name', CardType.SUSPECT, 'TEST222ID')
test_card3 = Card('Test Card 3 Name', CardType.SUSPECT, 'TEST333ID')
test_card4 = Card('Test Card 4 Name', CardType.SUSPECT, 'TEST444ID')
test_hand = Hand([test_card1, test_card2])

def test_init():
    assert type(test_hand) is Hand

def test_serialize():
    hand_serial = test_hand.serialize()
    assert hand_serial.find(f'"TEST111ID": "{test_card1.serialize()}", "TEST222ID": "{test_card2.serialize()}"')
def test_deserialize():
    hand_serial = test_hand.serialize()
    hand_deserial = Hand.deserialize(hand_serial)
    assert type(hand_deserial) is Hand
    assert hand_deserial == test_hand

def test_str():
    assert str(test_hand) == 'Test Card 1 Name, Test Card 2 Name'

def test_add_card():
    assert len(test_hand.get_cards()) == 2
    test_hand.add_card(test_card3)
    assert len(test_hand.get_cards()) == 3
    assert str(test_hand) == (
        'Test Card 1 Name, Test Card 2 Name, Test Card 3 Name')

def test_contains_card():
    assert test_hand.contains_card(test_card2)
    assert not test_hand.contains_card(test_card4)


def test_get_cards():
    for list_card in test_hand.get_cards():
        assert test_hand.contains_card(list_card)
