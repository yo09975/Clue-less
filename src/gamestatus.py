"""gamestatus.py."""
from enum import Enum


class GameStatus(Enum):
    """Enumeration of a Game's status.

    GameStatus class in the Game Management Subsystem. Contains ####
    enumeration values to set a Game's status.

    Attributes:
    LOBBY - Denotes a game is in the initialization/waiting state
    MOVE_PIECE - Denotes a game has a player completing a move
    MAKE_SUGG - Denotes a game has a player making a suggestion
    ANSWER_SUGG - Denotes a game is processing a suggestion answer
    MAKE_ACCUS - Denotes a game has a player making an accusation

    """
    LOBBY = 1
    MOVE_PIECE = 2
    MAKE_SUGG = 3
    ANSWER_SUGG = 4
    MAKE_ACCUS = 5
