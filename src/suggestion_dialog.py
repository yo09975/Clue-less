"""suggestion_dialog.py"""
from src.dialog import Dialog

class SuggestionDialog(Dialog):
    """
    A dialog that has 3 Pickers corresponding to Characters, Rooms, and Weapons


    character_picker = None  # picker object representing all possible suspects
    room_picker = None  # picker object representing all possible rooms
    weapon_picker = None    # picker object representing all possible weapons
    """

    def __init__(self, message, card_type, left_button, right_button, x, y, w, h):
        """Constructor for SuggestionDialog that accepts a String and Enum"""
        self.__card_type = card_type

        self._character_picker = Picker([])
        self._room_picker = Picker([])
        self._weapon_picker = Picker([])

        super(SuggestionDialog, self).__init__(message, left_button, right_button, x, y, w, h)


    def clear_selection(self):
        """Clear all current selections"""
        return True
