"""gamecontroller.py."""
from src.gamestate import GameState
from src.suggestion_engine import SuggestionEngine
from src.movementengine import MovementEngine
from src.message import Message
from src.message import MessageType
from src.gamestatus import GameStatus


class GameController(object):
    """Overall controller of a game used to update Game State.

    GameController class in the Game Management Subsystem.  Takes inputs and
    outputs from other controllers and updates the GameState.  The central
    piece is a finite state machine, which has all of the game workflow built

    Attributes:
    _current_game - Instance of GameState object representing the current game
    _suggest_engine - Instance of SuggestionEngine object for processing
                     suggestions
    _move_engine - Instance of MovementEngine object for processing moves

    """

    def __init__(self):
        """Constructor"""
        print('Constructor in GameController class')
        self._current_game = GameState()
        self._suggest_engine = SuggestionEngine(self._current_game)
        self._move_engine = MovementEngine()

    def get_game_state(self) -> GameState:
        """Returns GameState reference"""
        return self._current_game

    def get_suggest_engine(self) -> SuggestionEngine:
        """Returns SuggestionEngine reference"""
        return self._suggest_engine

    def get_move_engine(self) -> MovementEngine:
        """Returns MovementEngine reference"""
        return self._move_engine

    def read_message(self, message: Message):
        """Accepts a Message to process"""
        msg_type = message.get_msg_type()
        if msg_type == MessageType.MOVEMENT:
            self._current_game.set_state(GameStatus.MOVE_PIECE)
        elif msg_type == MessageType.SUGGESTION:
            self._current_game.set_state(GameStatus.MAKE_SUGG)
        elif msg_type == MessageType.SUGGESTION_RESP:
            self._current_game.set_state(GameStatus.ANSWER_SUGG)
        elif msg_type == MessageType.ACCUSATION:
            self._current_game.set_state(GameStatus.MAKE_ACCUS)
