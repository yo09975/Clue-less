"""test_gamecontroller.py"""
from src.gamecontroller import GameController
from src.network.message import Message
from src.network.message import MessageType
from src.gamestate import GameState
from src.gamestatus import GameStatus
from src.card import Card
from src.cardtype import CardType
from src.player import Player
from src.playerlist import PlayerList
from src.playerstatus import PlayerStatus

test_card1 = Card('Test Card 1 Name', CardType.SUSPECT, 'TEST111ID')
test_card2 = Card('Test Card 2 Name', CardType.SUSPECT, 'TEST222ID')
test_card3 = Card('Test Card 3 Name', CardType.WEAPON, 'TEST333ID')
test_card4 = Card('Test Card 4 Name', CardType.ROOM, 'TEST444ID')
test_card5 = Card('Test Card 5 Name', CardType.ROOM, 'TEST555ID') #Receives UUID TST123456
test_card6 = Card('Test Card 6 Name', CardType.ROOM, 'TEST666ID')
test_player1 = Player(test_card1)
test_player1.set_status(PlayerStatus.COMP)
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
test_plist1.add_player(test_player1)
test_plist1.add_player(test_player2)
test_plist1.add_player(test_player3)
test_plist1.add_player(test_player4)
test_plist1.add_player(test_player5)
test_plist1.add_player(test_player6)

gc = GameController()
"""Initial GameController Instance"""

leave_game_message = Message(
    'LEAVE GAME', MessageType.LEAVE_GAME, 'TEST555ID')

select_piece_message = Message(
    'TST123456', MessageType.SELECT_PIECE, 'TEST555ID')

start_game_message = Message(
    'TEST UUID', MessageType.START_GAME, 'TEST555ID')

movement_message = Message(
    'TEST UUID', MessageType.MOVEMENT, 'TEST555ID')

def test_leave_game():
    gc.get_game_state().set_state(GameStatus.WAIT_SUGG)
    assert gc.get_game_state().get_state() is GameStatus.WAIT_SUGG
    gc.read_message(leave_game_message)
    assert gc.get_game_state().get_state() is GameStatus.LOBBY

def test_select_piece():
    assert gc.get_game_state().get_state() is GameStatus.LOBBY
    gc.read_message(select_piece_message)
    assert gc.get_game_state().get_state() is GameStatus.LOBBY
    assert test_plist1.get_player('TEST555ID').get_uuid() is 'TST123456'

def test_start_game():
    gc.read_message(start_game_message)
    assert gc.get_game_state().get_state() is GameStatus.START_TURN
    assert gc.get_game_state().get_current_player() is test_player3

def test_movement():
