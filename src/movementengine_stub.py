"""movementengine_stub.py.

Stubs out MovementEngine so that other developers can write to its API.  Always
returns that a move is valid.
"""
from movementengine import MovementEngine


class MovementEngineStub(MovementEngine):
    """Stub.

    Stubs out MovementEngine so that other developers can write to its API.
    Always returns that a move is valid.
    """

    def is_valid_move(self, move):
        """Return whether move is valid. Always returns true."""
        return True
