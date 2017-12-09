"""test_player.py"""
import pytest
from src.player import Player
from src.card import Card
from src.cardtype import CardType
from src.hand import Hand
from src.location import Location
from src.playerstatus import PlayerStatus


test_card1 = Card('Miss Scarlet', CardType.SUSPECT)
test_card2 = Card('Colonel Mustard', CardType.SUSPECT)
test_card3 = Card('Knife', CardType.WEAPON)
test_card4 = Card('Hall', CardType.ROOM)
test_location1 = Location('Test Location 1', "1x1")
test_location2 = Location('Test Location 2', "1x2")
test_hand = Hand([test_card1, test_card2, test_card3, test_card4])
test_player = Player(test_card1)


def test_init():
    assert type(test_player) is Player
    assert test_player.get_card_id() == 'Miss Scarlet'
    with pytest.raises(ValueError):
        bad_card_player = Player(test_card3)


def test_str():
    assert str(test_player) == 'Player is playing as: Miss Scarlet'


def test_set_and_get_hand():
    assert len(test_player.get_hand().get_cards()) == 0
    test_player.set_hand(test_hand)
    assert test_player.get_hand() == test_hand
    assert type(test_player.get_hand()) == Hand


def test_set_and_get_character():
    assert test_player.get_character() == test_card1
    test_player.set_character(test_card2)
    assert test_player.get_character() == test_card2
    assert type(test_player.get_character()) == Card
    assert str(test_player) == 'Player is playing as: Colonel Mustard'


def test_set_and_get_status():
    assert test_player.get_status() == PlayerStatus.COMP
    assert type(test_player.get_status()) is PlayerStatus
    test_player.set_status(PlayerStatus.ACTIVE)
    assert test_player.get_status() == PlayerStatus.ACTIVE
    assert type(test_player.get_status()) is PlayerStatus


def test_set_and_get_locations():
    assert test_player.get_current_location() is None
    assert test_player.get_previous_location() is None
    test_player.set_location(test_location1._key)
    assert test_player.get_current_location() == test_location1._key
    assert test_player.get_previous_location() == test_location1._key
    assert type(test_player.get_current_location()) is str
    test_player.set_location(test_location2._key)
    assert test_player.get_current_location() == test_location2._key
    assert test_player.get_previous_location() == test_location1._key


def test_set_and_get_card_id():
    assert test_player.get_card_id() == 'Miss Scarlet'
    assert type(test_player.get_card_id()) is str
    test_player.set_card_id('Mrs. White')
    assert test_player.get_card_id() == 'Mrs. White'


def test_set_and_get_uuid():
    test_player.set_uuid('TEST UUID')
    assert test_player.get_uuid() == 'TEST UUID'
    assert type(test_player.get_uuid()) is str


def test_set_and_get_was_transferred():
    assert not test_player.get_was_transferred()
    assert type(test_player.get_was_transferred()) is bool
    test_player.set_was_transferred(True)
    assert test_player.get_was_transferred()
