"""game_app.py"""


class GameApp(object):
    """
    Triggered by controllers to update after a move or suggestion has been asked.
    Can also show new views due to user action (asking for a suggestion).  Extends UserInterface.
    """

    note_card_view = None   # two-dimensional array of button objects representing the note card information
    note_card = None    # a reference to the current note_card
    note_card_controller = None    # a reference to the NoteCardController to send clicks

    def __init__(self, note_card_view, note_card, note_card_controller):
        self.__note_card_view = note_card_view
        self.__note_card = note_card
        self.__note_card_controller = note_card_controller

    def disconnect(self):
        return True
