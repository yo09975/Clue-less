"""test_card.py"""
from src.card import Card
from src.cardtype import CardType


test_card = Card('Miss Scarlet', CardType.SUSPECT)


def test_init():
    assert type(test_card) is Card


def test_str():
    assert str(test_card) == 'Miss Scarlet CardType.SUSPECT'

def test_get_id():
    assert str(test_card.get_id()) == 'Miss Scarlet'


def test_get_type():
    testvar = test_card.get_type()
    assert testvar == CardType.SUSPECT
    assert type(testvar) is CardType


def test_serialization():
    payload = test_card.serialize()
    test_card2 = Card.deserialize(payload)
    assert payload == test_card2.serialize()
