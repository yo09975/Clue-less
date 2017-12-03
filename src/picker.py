"""picker.py"""
from src.pyview import PyView

class Picker(PyView):
    """A list of toggles, where only one toggle can be selected at any given time

    choices = None  # an array of toggle objects that contains the choices
    key = None
    """

    def __init__(self, choices):
        """Constructor that accepts an array of card objects to initialize the Picker object"""
        super(Picker, self).__init__(x, y, w, h)
        self._choices = choices
        for c in self._choices:
            self.add_view(c)


    def disable_button(self, key):
        """Accepts an integer identifying the button to disable"""
        self._choices[key].set_enabled(False)


    def deselect_all_except(self, key):
        """Accepts an integer identifying the button to select"""
        for i in range(len(self._choices)):
            if i == key:
                next
            self._choices[i].set_selected(False)


    def get_selected(self):
        """Returns a Card object that represents the selected item"""
        for t in self._choices:
            if t._is_selected:
                return t  # TODO determine what this should return
