"""test_deck.py"""
from src.card import Card
from src.cardtype import CardType
from src.deck import Deck


test_card1 = Card('Test Card 1 Name', CardType.SUSPECT, 'TEST111ID')
test_card2 = Card('Test Card 2 Name', CardType.SUSPECT, 'TEST222ID')
test_card3 = Card('Test Card 3 Name', CardType.SUSPECT, 'TEST333ID')
test_card4 = Card('Test Card 4 Name', CardType.SUSPECT, 'TEST444ID')
test_deck1 = Deck([test_card1, test_card2])
test_deck2 = Deck([test_card3, test_card4])


def test_init():
    assert type(test_deck1) is Deck


def test_str():
    assert str(test_deck1) == 'Test Card 1 Name, Test Card 2 Name'


def test_add_card():
    assert len(test_deck1.get_cards()) == 2
    test_deck1.add_card(test_card3)
    assert len(test_deck1.get_cards()) == 3
    assert str(test_deck1) == (
        'Test Card 1 Name, Test Card 2 Name, Test Card 3 Name')


def test_deal():
    assert len(test_deck1.get_cards()) == 3
    assert test_deck1.deal() == test_card3
    assert len(test_deck1.get_cards()) == 2


def test_contains_card():
    assert test_deck1.contains_card(test_card1)
    assert not test_deck1.contains_card(test_card3)


def test_add():
    assert len(test_deck1.get_cards()) == 2
    assert len(test_deck2.get_cards()) == 2
    test_deck3 = test_deck1 + test_deck2
    assert len(test_deck3.get_cards()) == 4
    for list_card in test_deck1.get_cards():
        assert test_deck3.contains_card(list_card)
    for list_card in test_deck2.get_cards():
        assert test_deck3.contains_card(list_card)


def test_shuffle():
    test_deck3 = test_deck1 + test_deck2
    assert str(test_deck3) == (
      'Test Card 1 Name, Test Card 2 Name, Test Card 3 Name, Test Card 4 Name')
    test_deck3.shuffle()
    assert str(test_deck3) != (
      'Test Card 1 Name, Test Card 2 Name, Test Card 3 Name, Test Card 4 Name')


def test_get_cards():
    new_hand = test_deck1.get_cards()
    for list_card in new_hand:
        assert test_deck1.contains_card(list_card)
