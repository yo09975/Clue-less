"""Dialog.py"""


class Dialog(object):
    """
    Pop-up that contains a message and has two buttons.  Initiated with references
    to the actions that should be taken for each button.
    """

    message = None  # a string representing the message to display
    left_button = None  # a button representing a command
    right_button = None # a button representing a command

    def __init__(self, message, left_button, right_button):
        """Constructor for Dialog which accepts two Button objects and a String"""
        self.__message = message
        self.__left_button = left_button
        self.__right_button = right_button


class SuggestionDialog(Dialog):
    """
    A dialog that has 3 Pickers corresponding to Characters, Rooms, and Weapons
    """

    character_picker = None  # picker object representing all possible suspects
    room_picker = None  # picker object representing all possible rooms
    weapon_picker = None    # picker object representing all possible weapons
    confirm_button = None   # button object that confirms selection
    cancel_button = None    # button object that cancels selection

    def __init__(self, message, card_type, left_button, right_button):
        """Constructor for SuggestionDialog that accepts a String and Enum"""
        super().__init__(message, left_button, right_button)    # recommended by PyCharm
        self.__message = message
        self.__card_type = card_type
        self.__cancel_button = left_button
        self.__confirm_button = right_button

    def clear_selection(self):
        """Clear all current selections"""
        return True


class CharacterDialog(SuggestionDialog):
    """
    Overrides the appropriate functionality so that a user can see which characters
    are available and pick one, then start a game
    """
    print('Cheeseburger')
