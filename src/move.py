"""move.py.

Contains the piece to move, and the destination for it to be moved to.
"""
from src.location import Location


class Move:
    """The piece to move, and the destination for it to be moved to."""

    def __init__(self, character, destination):
        if type(destination) is not str:
            raise TypeError('destination should be type str, not Location')

        """Initialize."""
        self._character = character
        self._destination = destination

    def get_character_id(self):
        """Return character_id of character to be moved."""
        return self._character

    def get_destination(self):
        """Return destination id."""
        return self._destination
