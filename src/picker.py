from src.toggle import Toggle
from src.view import View


class Picker(View):


    def __init__(self, choices, x, y, w, h):
        super(Picker, self).__init__(x, y, w, h)

        self._choices = choices
        self._toggles = []
        # Draw buttons and assign functionality
        for i, c in enumerate(choices):
            toggle = Toggle(self._coords[0], self._coord[0] + 50 * i, 200, 40)

            def click_action(args):
                toggle = args['t']
                picker = args['p']
                index = args['i']
                if toggle.get_selected():
                    picker.deselect_all_except(index)

            def default_action(args):
                toggle = args['t']
                if toggle.get_selected():
                    toggle.fill(pygame.Color(255, 0, 0))
                    toggle.set_alpha(100)
                else:
                    toggle.set_alpha(0)

            toggle.set_on_click(click_action, {'t': toggle, 'p': self, 'i': i})
            toggle.set_default_action(default_action, {'t': toggle})
            self._toggles.append(toggle)

    def disable_button(self, key):
        self._toggles[key].set_enabled(False)


    def deselect_all_except(self, key):
        for i, t in enumerate(self._toggles):
            if i != key:
                t.set_selected(False)


    def get_selected(self):
        for i, t in enumerate(self._toggles):
            if t.get_selected():
                return self._choices[i]

        # If you haven't found a selected toggle, return False
        return False
