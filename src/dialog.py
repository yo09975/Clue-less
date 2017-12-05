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
        
        self._top_button = Button(self._coords[0] + 681, self._coords[1] + 396, 200, 40)
        self.add_view(self._top_button)

        self._bottom_button = Button(self._coords[0] + 681, self._coords[1] + 446, 200, 40)
        self.add_view(self._bottom_button)

    def get_top_button(self):
        return self._top_button

    def get_bottom_button(self):
        return self._bottom_button
