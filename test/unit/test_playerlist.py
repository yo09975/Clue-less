"""test_playerlist.py"""
import pytest
from src.playerlist import PlayerList
from src.player import Player
from src.card import Card
from src.cardtype import CardType
from src.playerstatus import PlayerStatus

test_card1 = Card('Colonel Mustard', CardType.SUSPECT)
test_card2 = Card('Miss Scarlet', CardType.SUSPECT)
test_card3 = Card('Professor Plum', CardType.SUSPECT)
test_card4 = Card('Mrs. White', CardType.SUSPECT)
test_card5 = Card('Mr. Green', CardType.SUSPECT)
test_card6 = Card('Mrs. Peacock', CardType.SUSPECT)
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
    assert test_plist1 is test_plist2
    assert test_plist1 == test_plist2
def test_add_player():
    # If another test has populated the playerlist, clear it
    if (len(test_plist1) != 0):
        test_plist1.clear()

    # Check that after a clear(), both lists are the same length
    assert len(test_plist1) == len(test_plist2)

    # Check that adding a player increases the size of the list
    test_plist1.add_player(test_player1)
    assert len(test_plist1) ==  1

    # Check that adding a player increases the size of the list for
    # both references
    test_plist2.add_player(test_player2)
    assert len(test_plist1) == 2
    assert len(test_plist2) == 2

    # Add four more players and check that the count is correct
    test_plist1.add_player(test_player3)
    test_plist2.add_player(test_player4)
    test_plist1.add_player(test_player5)
    test_plist2.add_player(test_player6)
    assert len(test_plist1.get_players()) == 6

    # Attempt to add one more player (more than __MAX_PLAYERS)
    with pytest.raises(IndexError):
        test_plist1.add_player(test_player6)

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
    assert test_plist1.get_player('BAD ID') is None
    assert test_plist1.get_player('Professor Plum') == test_player3
    assert type(test_plist1.get_player('Professor Plum')) is Player

def test_setup():
    test_plist1.clear()
    test_plist1.setup()
    assert test_plist1.get_player_by_index(0).get_current_location() == "4x0"
    assert test_plist1.get_player_by_index(1).get_current_location() == "6x2"
    assert test_plist1.get_player_by_index(2).get_current_location() == "4x6"
    assert test_plist1.get_player_by_index(3).get_current_location() == "2x6"
    assert test_plist1.get_player_by_index(4).get_current_location() == "0x4"
    assert test_plist1.get_player_by_index(5).get_current_location() == "0x2"
