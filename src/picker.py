"""Picker.py"""


class Picker(object):
    """A list of toggles, where only one toggle can be selected at any given time"""

    choices = None  # an array of toggle objects that contains the choices
    key = None

    def __init__(self, choices):
        """Constructor that accepts an array of card objects to initialize the Picker object"""
        self.__choices = choices

    def disable_button(self, key):
        """Accepts an integer identifying the button to disable"""
        return True

    def deselect_all_except(self, key):
        """Accepts an integer identifying the button to select"""
        return True

    def get_selected(self):
        """Returns a Card object that represents the selected item"""
        return True
