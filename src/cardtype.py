"""cardtype.py."""
from enum import Enum


class CardType(Enum):
    """Enumeration of a Card's type (Suspect, Room, or Weapon).

    CardType class in the Game Management Subsystem. Contains three
    enumeration values to set a Card's type.

    Attributes:
    SUSPECT - Denotes a character card
    ROOM - Denotes a room card
    WEAPON - Denotes a weapon card

    """
    SUSPECT = 1
    ROOM = 2
    WEAPON = 3
