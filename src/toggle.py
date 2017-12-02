"""toggle.py"""


class Toggle(Button):
    """
    Extension of Button that can be turned on or off
    """

    is_selected = None  # Boolean representing if the Toggle is selected

    def set_selected(self, is_selected):
        """Accepts Boolean to set if the Toggle is selected or not"""
        return True

    def flip(self):
        """Changes the current state of the Boolean is_selected to the opposite and returns a Boolean"""
        return True
