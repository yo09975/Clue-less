"""playerstate.py.

The state of the user interface.
"""
from enum import Enum

class PlayerState(Enum):
        SELECT_PLAYER = 1
        WAIT_FOR_TURN = 2
        ANSWER_SUGGESTION = 3
        MY_TURN = 4
        POST_SUGGESTION = 5
        POST_SUGGESTION_ANSWER = 6
        POST_MOVE = 7
