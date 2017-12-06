"""test_card.py"""
from src.card import Card
from src.cardtype import CardType


test_card = Card('Test Card Name', CardType.SUSPECT, 'TEST123ID')


def test_init():
    assert type(test_card) is Card


def test_str():
    assert str(test_card) == 'Test Card Name CardType.SUSPECT TEST123ID'


def test_get_name():
    assert str(test_card.get_name()) == 'Test Card Name'


def test_get_id():
    assert str(test_card.get_id()) == 'TEST123ID'


def test_get_type():
    testvar = test_card.get_type()
    assert testvar == CardType.SUSPECT
    assert type(testvar) is CardType


def test_serialization():
    payload = test_card.serialize()
    test_card2 = Card.deserialize(payload)
    assert payload == test_card2.serialize()
