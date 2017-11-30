"""test_gamecontroller.py"""
from src.gamecontroller import GameController
from src.message import Message
from src.message import MessageType
from src.gamestate import GameState
from src.gamestatus import GameStatus

gc = GameController()
"""Initial GameController Instance"""


def test_read_message():
    movement_message = Message(
        'Test UUID', MessageType.MOVEMENT, 'Test Movement Message Payload')
    suggestion_message = Message(
        'Test UUID', MessageType.SUGGESTION, 'Test Suggestion Message Payload')
    suggestion_resp_message = Message(
        'Test UUID', MessageType.SUGGESTION_RESP,
        'Test Suggestion Response Message Payload')
    accusation_message = Message(
        'Test UUID', MessageType.ACCUSATION, 'Test Accusation Message Payload')

    """Default GameStatus"""
    assert gc.get_game_state().get_state() is GameStatus.LOBBY

    """Send Message with MOVEMENT msg_type to GameController"""
    gc.read_message(movement_message)
    assert gc.get_game_state().get_state() is GameStatus.MOVE_PIECE

    """Send Message with MOVEMENT msg_type to GameController"""
    gc.read_message(suggestion_message)
    assert gc.get_game_state().get_state() is GameStatus.MAKE_SUGG

    """Send Message with MOVEMENT msg_type to GameController"""
    gc.read_message(suggestion_resp_message)
    assert gc.get_game_state().get_state() is GameStatus.ANSWER_SUGG

    """Send Message with MOVEMENT msg_type to GameController"""
    gc.read_message(accusation_message)
    assert gc.get_game_state().get_state() is GameStatus.MAKE_ACCUS
