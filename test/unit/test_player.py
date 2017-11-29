"""test_player.py"""
from src.player import Player
from src.card import Card
from src.cardtype import CardType
from src.hand import Hand
from src.location import Location
from src.playerstatus import PlayerStatus


test_card1 = Card('Test Card 1 Name', CardType.SUSPECT, 'TEST111ID')
test_card2 = Card('Test Card 2 Name', CardType.SUSPECT, 'TEST222ID')
test_card3 = Card('Test Card 3 Name', CardType.WEAPON, 'TEST333ID')
test_card4 = Card('Test Card 4 Name', CardType.ROOM, 'TEST444ID')
test_location1 = Location('Test Location 1', "1x1")
test_location2 = Location('Test Location 2', "1x2")
test_hand = Hand([test_card1, test_card2, test_card3, test_card4])
test_player = Player(test_card1)


def test_init():
    assert type(test_player) is Player
    assert test_player.get_token() == 'TEST111ID'


def test_str():
    assert str(test_player) == 'Player is playing as: Test Card 1 Name'


def test_set_and_get_hand():
    if test_player.get_hand() is None:
        assert True
    else:
        assert False
    test_player.set_hand(test_hand)
    assert test_player.get_hand() == test_hand
    assert type(test_player.get_hand()) == Hand


def test_set_and_get_character():
    assert test_player.get_character() == test_card1
    test_player.set_character(test_card2)
    assert test_player.get_character() == test_card2
    assert type(test_player.get_character()) == Card
    assert str(test_player) == 'Player is playing as: Test Card 2 Name'


def test_set_and_get_status():
    assert test_player.get_status() == PlayerStatus.COMP
    assert type(test_player.get_status()) is PlayerStatus
    test_player.set_status(PlayerStatus.ACTIVE)
    assert test_player.get_status() == PlayerStatus.ACTIVE
    assert type(test_player.get_status()) is PlayerStatus


def test_set_and_get_locations():
    if test_player.get_current_location() is None:
        assert True
    else:
        assert False
    if test_player.get_previous_location() is None:
        assert True
    else:
        assert False
    test_player.set_location(test_location1)
    assert test_player.get_current_location() == test_location1
    assert test_player.get_previous_location() == test_location1
    assert type(test_player.get_current_location()) is Location
    test_player.set_location(test_location2)
    assert test_player.get_current_location() == test_location2
    assert test_player.get_previous_location() == test_location1


def test_set_and_get_token():
    assert test_player.get_token() == 'TEST111ID'
    assert type(test_player.get_token()) is str
    test_player.set_token('NEW TOKEN')
    assert test_player.get_token() == 'NEW TOKEN'


def test_set_and_get_was_transferred():
    assert not test_player.get_was_transferred()
    assert type(test_player.get_was_transferred()) is bool
    test_player.set_was_transferred(True)
    assert test_player.get_was_transferred()
