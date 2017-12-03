"""dialog.py"""
from src.pyview import PyView

class Dialog(PyView):
    """
    Pop-up that contains a message and has two buttons.  Initiated with references
    to the actions that should be taken for each button.


    message = None  # a string representing the message to display
    left_button = None  # a button representing a command
    right_button = None # a button representing a command
    """

    def __init__(self, message, left_button, right_button, x, y, w, h):
        """Constructor for Dialog which accepts two Button objects and a String"""
        self._message = message
        self._left_button = left_button
        self._right_button = right_button
        super(Dialog, self).__init__(x, y, w, h)
