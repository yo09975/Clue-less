"""playerstatus.py."""
from enum import Enum


class PlayerStatus(Enum):
    """Enumeration of a Player's status type (COMP, ACTIVE, LOST).

    PlayerStatus class in the Game Management Subsystem. Contains three
    enumeration values to set a Player's status.

    Attributes:
    COMP - Denotes a player is not controlled by a human (default)
    ACTIVE - Denotes a player is active in the game
    LOST - Denotes a player has given an incorrect accusation and lost

    """
    COMP = 1
    ACTIVE = 2
    LOST = 3
