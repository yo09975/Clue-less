"""board_stub.py.

Stubs out Board so that it returns "hall" whenever you invoke get_location.
"""
from board import Board


class BoardStub(Board):
        """The gameboard.

        Stubs out Board so that it returns "hall" whenever you invoke
        get_location.
        """

        def get_location(self, location_id):
            """Return 'hall' regardless of input."""
            return "hall"
