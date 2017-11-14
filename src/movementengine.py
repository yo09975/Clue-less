"""movementengine.py.

Receives requests from Game Controller to check validity of a move, or to make
the move no matter what. Uses suggestions, movement requests, etc., to find
pieces on the board, move them to their new location, and remove them from
their old location. Will also determine if new location is at capacity or not.
Returns success to Game Controller. Error handling includes admonishing Player
for attempting invalid move.
"""
from board import Board


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
        return

    def do_move(self, move):
        """Accept a Move and process it."""
        return
