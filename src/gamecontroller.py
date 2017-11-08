class GameController(object):
    """Overall controller of a game used to update Game State.

    GameController class in the Game Management Subsystem.  Takes inputs and
    outputs from other controllers and updates the GameState.  The central
    piece is a finite state machine, which has all of the game workflow built
    """

    current_game = None
    """Instance of GameState object representing the current game"""
    suggest_engine = None
    """Instance of SuggestionEngine object for processing suggestions"""
    move_engine = None
    """Instance of MovementEngine object for processing moves"""

    def __init__(self):
        """Constructor"""
        print('Constructor in GameController class')

    def read_message(message):
        """Accepts a Message to process"""
        print('read_message method in GameController class')
