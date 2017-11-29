"""test_playerlist.py"""
from src.playerlist import PlayerList
from src.player import Player
from src.card import Card
from src.cardtype import CardType
from src.playerstatus import PlayerStatus
from src.gamestate import GameState
from src.suggestion import Suggestion
from src.gamestatus import GameStatus


test_card1 = Card('Test Card 1 Name', CardType.SUSPECT, 'TEST111ID')
test_card2 = Card('Test Card 2 Name', CardType.SUSPECT, 'TEST222ID')
test_card3 = Card('Test Card 3 Name', CardType.WEAPON, 'TEST333ID')
test_card4 = Card('Test Card 4 Name', CardType.ROOM, 'TEST444ID')
test_card5 = Card('Test Card 5 Name', CardType.ROOM, 'TEST555ID')
test_card6 = Card('Test Card 6 Name', CardType.ROOM, 'TEST666ID')

test_gamestate = GameState()
player_list = PlayerList()
players = player_list.get_players()
test_player_0 = players[0]
test_player_1 = players[1]
test_player_2 = players[2]
test_player_3 = players[3]
test_player_4 = players[4]
test_player_5 = players[5]

test_player_0.set_status(PlayerStatus.ACTIVE)
test_player_1.set_status(PlayerStatus.COMP)
test_player_2.set_status(PlayerStatus.ACTIVE)
test_player_3.set_status(PlayerStatus.LOST)
test_player_4.set_status(PlayerStatus.COMP)
test_player_5.set_status(PlayerStatus.COMP)

test_solution = Suggestion(test_card4, test_card3, test_card1)


def test_init():
    assert type(test_gamestate) is GameState


def test_next_turn():
    assert test_gamestate.get_current_player() == 0
    assert test_gamestate.next_turn() == test_player_2
    assert test_gamestate.get_current_player() == 2
    assert type(test_gamestate.next_turn()) is Player
    assert test_gamestate.get_current_player() == 0


def test_get_and_set_state():
    assert test_gamestate.get_state() == GameStatus.LOBBY
    test_gamestate.set_state(GameStatus.MOVE_PIECE)
    assert test_gamestate.get_state() == GameStatus.MOVE_PIECE
    assert type(test_gamestate.get_state()) is GameStatus


def test_get_and_set_solution():
    assert test_gamestate.get_solution() is None
    test_gamestate.set_solution(test_solution)
    assert test_gamestate.get_solution() == test_solution
    assert type(test_gamestate.get_solution()) is Suggestion


def test_get_and_set_current_player():
    test_gamestate.set_current_player(1)
    assert test_gamestate.get_current_player() == 1
    assert type(test_gamestate.get_current_player()) is int
    test_gamestate.set_current_player(0)
    assert test_gamestate.get_current_player() == 0
