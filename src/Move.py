"""Move.py."""


class Move:
    """Move to be executed."""

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
