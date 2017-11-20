"""movementengine.py.

Receives requests from Game Controller to check validity of a move, or to make
the move no matter what. Uses suggestions, movement requests, etc., to find
pieces on the board, move them to their new location, and remove them from
their old location. Will also determine if new location is at capacity or not.
Returns success to Game Controller. Error handling includes admonishing Player
for attempting invalid move.
"""
from src.board import Board
from src.playerlist import PlayerList


class MovementEngine:
    """Validate and execute moves.

    Receives requests from Game Controller to check validity of a move, or to
    make the move no matter what. Uses suggestions, movement requests, etc., to
    find pieces on the board, move them to their new location, and remove them
    from their old location. Will also determine if new location is at capacity
    or not. Returns success to Game Controller. Error handling includes
    admonishing Player for attempting invalid move.
    """

    def __init__(self):
        """Initialize."""
        self._board = Board()

    def is_valid_move(self, move):
        """Return whether move is valid."""

        # Get player's current location
        player_list = PlayerList()
        player = player_list.get_player(move.get_charcter_id())
        from_location = player.get_current_location()

        # Get destination location from board
        destination = self._board.get_location(move.get_destination())

        # Check to see if destination has occupancy
        if not destination.is_available():
            return False

        # Check to see if destination is a neighbor of location
        return from_location.is_neighbor(destination)

    def do_move(self, move):
        """Accept a Move and process it."""

        # Get the player's current location
        player_list = PlayerList()
        player = player_list.get_player(move.get_charcter_id())
        from_location = player.get_current_location()

        # Execute move on board and update player location
        self._board.move(from_location._key, move.get_destination())
        dest_location = self._board.get_location(move.get_destination())
        player.set_location(dest_location)

        return
