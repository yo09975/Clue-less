"""UserInterface.py"""


class UserInterface(object):
    """
    Defines interface between networking subsystem and the UI.  Game State will
    provide necessary information to be displayed on the UI (Game State, Game Board)
    """

    game_state = None   # reference to the GameState representing the current game
    board = None    # reference to the game board

    def __init__(self, game_state, board):
        self.__game_state = game_state
        self.__board = board

    def update():
        return True
