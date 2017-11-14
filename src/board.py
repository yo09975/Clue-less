"""board.py.

A map that allows the system to a Location on the Board by either its
coordinates on the grid, or by the room identifier.
"""


class Board:
    """The gameboard.

    A map that allows the system to a Location on the Board by either its
    coordinates on the grid, or by the room identifier.
    """

    def __init__(self):
        """Initialize."""
        self._locations = {}

    def move(self, from_location, to_location):
        """Move a player from one location and to another."""
        return

    def get_location(self, location_id):
        """Return a location from either a coordinate string or room id."""
        return
