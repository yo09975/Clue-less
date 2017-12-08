from src.toggle import Toggle
from src.view import View
import pygame

class CharacterPicker(View):


    def __init__(self, choices, x, y):

        w = 781
        h = 451

        super(CharacterPicker, self).__init__(x, y, w, h)
        self._choices = choices
        self._toggles = []
        # Draw buttons and assign functionality
        for i, c in enumerate(choices):
            x_pos = (i % 3) * 240 + self._coords[0]
            y_pos = int(i/3) * 200 + self._coords[1]

            toggle = Toggle(x_pos, y_pos, 200, 190)

            def click_action(args):
                toggle = args['t']
                picker = args['p']
                index = args['i']
                if toggle.get_selected():
                    picker.deselect_all_except(index)
                    # Call the on_changed function
                    try:
                        picker._on_change_function(picker._on_change_args)
                    except AttributeError:
                        pass

            def default_action(args):
                toggle = args['t']
                if toggle.get_selected():
                    toggle.fill(pygame.Color(255, 0, 0))
                    toggle.set_alpha(100)
                else:
                    toggle.fill(pygame.Color(255, 0, 0))
                    toggle.set_alpha(0)

            def disabled_action(args):
                args['b'].set_alpha(255)
                args['b'].fill(pygame.Color(121, 121, 121))

            toggle.set_on_click(click_action, {'t': toggle, 'p': self, 'i': i})
            toggle.set_default_action(default_action, {'t': toggle})
            toggle.set_disabled_action(disabled_action, {'b': toggle})
            self._toggles.append(toggle)
            self.add_view(toggle)

    def disable_button(self, key):
        self._toggles[key].set_enabled(False)


    def deselect_all_except(self, key):
        for i, t in enumerate(self._toggles):
            if i != key:
                t.set_selected(False)

    def enable_all(self):
        for t in self._toggles:
            t.set_enabled(True)

    def get_selected(self):
        for i, t in enumerate(self._toggles):
            if t.get_selected():
                return self._choices[i]

        # If you haven't found a selected toggle, return False
        return False

    def set_on_changed(self, function, args):
        ## Set the method that is called when a toggle in the picker changes
        self._on_change_function = function
        self._on_change_args = args
