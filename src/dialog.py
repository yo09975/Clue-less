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
