"""toggle.py.

A button that toggles on and off whenever it's clicked.
"""
from src.button import Button

class Toggle(Button):
    def __init__(self, x, y, w, h):
        self._is_selected = False
        super(Toggle, self).__init__(x, y, w, h)

    def click(self):
        """Overide Button click to switch is_selected"""
        self.flip()
        super(Toggle, self).click()

    def set_selected(self, is_selected):
        """Accepts Boolean to set if the Toggle is selected or not"""
        self._is_selected = is_selected
        return self._is_selected

    def flip(self):
        self._is_selected = not self._is_selected
        return self._is_selected

    def get_selected(self):
        return self._is_selected
