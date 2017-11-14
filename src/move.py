"""move.py.

Contains the piece to move, and the destination for it to be moved to.
"""


class Move:
    """The piece to move, and the destination for it to be moved to."""

    def __init__(self, character, destination):
        """Initialize."""
        self._character = character
        self._destination = destination

    def get_charcter_id(self):
        """Return character_id of character to be moved."""
        return self._character

    def get_destionation(self):
        """Return destination id."""
        return self._destination
