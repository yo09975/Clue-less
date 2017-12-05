"""test_playerlist.py"""
import pytest
from src.playerlist import PlayerList
from src.player import Player
from src.card import Card
from src.cardtype import CardType
from src.playerstatus import PlayerStatus
from src.gamestate import GameState

test_card1 = Card('Test Card 1 Name', CardType.SUSPECT, 'TEST111ID')
test_card2 = Card('Test Card 2 Name', CardType.SUSPECT, 'TEST222ID')
test_card3 = Card('Test Card 3 Name', CardType.WEAPON, 'TEST333ID')
test_card4 = Card('Test Card 4 Name', CardType.ROOM, 'TEST444ID')
test_card5 = Card('Test Card 5 Name', CardType.ROOM, 'TEST555ID')
test_card6 = Card('Test Card 6 Name', CardType.ROOM, 'TEST666ID')
test_player1 = Player(test_card1)
test_player1.set_status(PlayerStatus.ACTIVE)
test_player2 = Player(test_card2)
test_player2.set_status(PlayerStatus.COMP)
test_player3 = Player(test_card3)
test_player3.set_status(PlayerStatus.ACTIVE)
test_player3.set_uuid('TEST UUID')
test_player4 = Player(test_card4)
test_player4.set_status(PlayerStatus.LOST)
test_player5 = Player(test_card5)
test_player5.set_status(PlayerStatus.COMP)
test_player6 = Player(test_card6)
test_player6.set_status(PlayerStatus.COMP)
test_player7 = Player(test_card1)
test_plist1 = PlayerList()
test_plist2 = PlayerList()


def test_init():
    assert type(test_plist1) is PlayerList
    assert type(test_plist2) is PlayerList
    assert test_plist1.get_instance() == test_plist2.get_instance()


def test_add_player():

    # Create a baseline off of which to test player counts
    tare = len(test_plist1.get_players())

    test_plist1.add_player(test_player1)
    assert len(test_plist1.get_players()) == tare + 1
    test_plist2.add_player(test_player2)
    assert len(test_plist1.get_players()) == tare + 2
    assert len(test_plist2.get_players()) == tare + 2
    test_plist1.add_player(test_player3)
    test_plist2.add_player(test_player4)
    test_plist1.add_player(test_player5)
    test_plist2.add_player(test_player6)
    assert len(test_plist1.get_players()) == tare + 6


def test_get_next_turn():
    """Out of Bounds Index returns Error"""
    with pytest.raises(IndexError):
        test_plist1.get_next_turn(-4)
    with pytest.raises(IndexError):
        test_plist1.get_next_turn(6)
    """Index 0 (Player 1) in, skips Player 2 which is COMP, returns Player 3"""
    assert test_plist1.get_next_turn(0) == test_player3
    """Index 2 (Player 3) in, skips Player 4 who LOST, skips Players 5 and 6
       who are COMP, returns Player 1"""
    assert test_plist1.get_next_turn(2) == test_player1
    """Confirm returning Player object"""
    assert type(test_plist1.get_next_turn(0)) is Player


def test_get_next_player():
    """Invalid Player Returns Error"""
    with pytest.raises(ValueError):
        test_plist1.get_next_player(test_player7)
    """Player 1 in, skips Player 2 since it is COMP, returns Player 3 who is
       ACTIVE"""
    assert test_plist1.get_next_player(test_player1) == test_player3
    """Player 3 in, returns Player 4 who is LOST"""
    assert test_plist1.get_next_player(test_player3) == test_player4
    """Player 4 in, skips Player 5 and 6 since they are COMP, returns Player 1
       who is ACTIVE"""
    assert test_plist1.get_next_player(test_player4) == test_player1
    """Confirm returning Player object"""
    assert type(test_plist1.get_next_player(test_player1)) is Player
    """Set Players 2 and 3 to COMP"""
    test_player3.set_status(PlayerStatus.COMP)
    test_player4.set_status(PlayerStatus.COMP)
    """Player 1 in, Skips all other Players because they're all COMP, returns
       None"""
    if test_plist1.get_next_player(test_player1) is None:
        assert True
    else:
        assert False


def test_get_players():

    assert test_plist1.get_players() == [test_player1, test_player2,
                                         test_player3, test_player4,
                                         test_player5, test_player6]
    assert type(test_plist1.get_players()) is list


def test_get_player():
    if test_plist1.get_player('BAD ID') is None:
        assert True
    else:
        assert False
    assert test_plist1.get_player("TEST333ID") == test_player3
    assert type(test_plist1.get_player('TEST333ID')) is Player


def test_serialize_locations():
    gs = GameState()
    pl = PlayerList()
    payload = pl.serialize()
    assert type(payload) is str
    # Ensure that Col. Mustard's starting location is serialized
    assert payload.find('"Colonel Mustard": "6x2"') != -1


def test_deserialize_locations():
    # Invoke GameState so that starting positions are initialized
    gs = GameState()
    pl = PlayerList()
    payload = pl.serialize()

    # Change Col. Mustard's location and test to see if serialization worked
    payload = payload.replace("6x2", "5x2")
    pl.deserialize(payload)
    COL = pl.get_player("Colonel Mustard")
    assert COL.get_current_location() == "5x2"
