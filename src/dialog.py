"""dialog.py.

Basic dialog with configurable buttons.
"""
import pygame
from src.view import View
from src.button import Button

class Dialog(View):
    def __init__(self, x, y):
        w = 900
        h = 500
        super(Dialog, self).__init__(x, y, w, h)

        self._top_button = Button(self._coords[0] + 685, self._coords[1] + 395, 200, 40)
        self.add_view(self._top_button)

        self._bottom_button = Button(self._coords[0] + 685, self._coords[1] + 445, 200, 40)
        self.add_view(self._bottom_button)

        self._success = False

    def get_top_button(self):
        return self._top_button

    def get_bottom_button(self):
        return self._bottom_button

    def set_success(self, success):
        self._success = success

    def get_success(self):
        """Returns True if the dialog was successfully Confirmed."""
        return self._success

    def set_is_visible(self, is_visible):
        super(Dialog, self).set_is_visible()
        if (is_visible):
            self._success = False
