"""toggle.py"""
from src.pybutton import PyButton

class Toggle(PyButton):
    """
    Extension of Button that can be turned on or off
    """

    def _init__(self, x, y, w, h):
        self._is_selected = None  # Boolean representing if the Toggle is selected
        super(Toggle, self).__init__(x, y, w, h)

    def set_selected(self, is_selected):
        """Accepts Boolean to set if the Toggle is selected or not"""
        self._is_selected = is_selected
        return self._is_selected

    def flip(self):
        self._is_selected = not self._is_selected
        return self._is_selected
