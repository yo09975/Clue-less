"""Button.py"""


class Button(object):
    """
    A rectangular region that performs certain actions if hovered over or clicked.
    Can be invisible, have a color background, or have a picture background.  Can be disabled.
    """

    click_action = None  # method object to be executed when the parent Button object is clicked
    hover_action = None  # method object to be executed when the parent Button object is hovered over
    is_enabled = None    # Boolean representing if the Button object is currently enabled

    def set_click_action(self, click_action):
        """Accepts a method to set what is executed when Button is clicked"""
        return True

    def set_hover_action(self, hover_action):
        """Accepts a method to set what is executed when Button is hovered over"""
        return True

    def set_enabled(self, is_enabled):
        """Accepts a Boolean to set whether a Button is enabled or not"""
        return True

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
