"""test_playerlist.py"""
from src.playerlist import PlayerList
from src.player import Player
from src.card import Card
from src.cardtype import CardType
from src.playerstatus import PlayerStatus


test_card1 = Card('Test Card 1 Name', CardType.SUSPECT, 'TEST111ID')
test_card2 = Card('Test Card 2 Name', CardType.SUSPECT, 'TEST222ID')
test_card3 = Card('Test Card 3 Name', CardType.WEAPON, 'TEST333ID')
test_card4 = Card('Test Card 4 Name', CardType.ROOM, 'TEST444ID')
test_card5 = Card('Test Card 5 Name', CardType.ROOM, 'TEST555ID')
test_card6 = Card('Test Card 6 Name', CardType.ROOM, 'TEST666ID')
test_player1 = Player(test_card1)
test_player2 = Player(test_card2)
test_player3 = Player(test_card3)
test_player4 = Player(test_card4)
test_player5 = Player(test_card5)
test_player6 = Player(test_card6)
test_plist1 = PlayerList()
test_plist2 = PlayerList()


def test_init():
    assert type(test_plist1) is PlayerList
    assert type(test_plist2) is PlayerList
    assert test_plist1.get_instance() == test_plist2.get_instance()


def test_add_player():
    test_plist1.add_player(test_player1)
    assert len(test_plist1.get_players()) == 1
    test_plist2.add_player(test_player2)
    assert len(test_plist1.get_players()) == 2
    assert len(test_plist2.get_players()) == 2
    test_plist1.add_player(test_player3)
    test_plist2.add_player(test_player4)
    test_plist1.add_player(test_player5)
    test_plist2.add_player(test_player6)
    assert len(test_plist1.get_players()) == 6


def test_get_next_turn():
    if test_plist1.get_next_turn(-4) is None:
        assert True
    else:
        assert False
    if test_plist1.get_next_turn(6) is None:
        assert True
    else:
        assert False
    assert test_plist1.get_next_turn(1) == test_player3
    assert test_plist1.get_next_turn(5) == test_player1
    assert type(test_plist1.get_next_turn(0)) is Player


def test_get_next_player():
    assert test_plist1.get_next_player(test_player1) == test_player2
    assert test_plist1.get_next_player(test_player6) == test_player1
    assert type(test_plist1.get_next_player(test_player1)) is Player


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
    assert test_plist1.get_player('TEST333ID') == test_player3
    assert type(test_plist1.get_player('TEST333ID')) is Player
