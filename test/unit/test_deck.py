"""test_deck.py"""
from src.card import Card
from src.cardtype import CardType
from src.deck import Deck


test_card1 = Card('Miss Scarlet', CardType.SUSPECT)
test_card2 = Card('Colonel Mustard', CardType.SUSPECT)
test_card3 = Card('Mrs. White', CardType.SUSPECT)
test_card4 = Card('Mr. Green', CardType.SUSPECT)
test_deck1 = Deck([test_card1, test_card2])
test_deck2 = Deck([test_card3, test_card4])


def test_init():
    assert type(test_deck1) is Deck


def test_str():
    assert str(test_deck1) == 'Miss Scarlet, Colonel Mustard'


def test_add_card():
    assert len(test_deck1.get_cards()) == 2
    test_deck1.add_card(test_card3)
    assert len(test_deck1.get_cards()) == 3
    assert str(test_deck1) == (
        'Miss Scarlet, Colonel Mustard, Mrs. White')


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
      'Miss Scarlet, Colonel Mustard, Mrs. White, Mr. Green')
    test_deck3.shuffle()
    assert str(test_deck3) != (
      'Test Card 1 Name, Test Card 2 Name, Test Card 3 Name, Test Card 4 Name')


def test_get_cards():
    new_hand = test_deck1.get_cards()
    for list_card in new_hand:
        assert test_deck1.contains_card(list_card)
