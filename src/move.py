"""move.py.

Contains the piece to move, and the destination for it to be moved to.
"""
import json
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

    def serialize(self):
        """ Convert a Move to JSON """
        move = {}
        move['character'] = self.get_character_id()
        move['destination'] = self.get_destination()
        return json.dumps(move)

    def deserialize(payload):
        """ Convert a JSON string to a Move """
        serial_move = json.loads(payload)
        return Move(serial_move['character'], serial_move['destination'])
