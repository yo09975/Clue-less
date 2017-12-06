"""button.py.

A view that supports configurable clicks and reactions.
"""

from src.view import View
import pygame


class Button(View):
    def __init__(self, x, y, w, h):
        self._is_enabled = True
        super(Button, self).__init__(x, y, w, h)

        # Use to debounce button
        self._pressed = False

    def draw(self, event, display):
        """Override View.draw() to allow for configurability of Button."""
        m = event.get_pos()
        coords = self._coords
        if (self._is_enabled):
            # If mouse is over button, process clicks and hoveraction
            if (coords[0] < m[0] < coords[0] + self.get_size()[0] and \
                coords[1] < m[1] < coords[1] + self.get_size()[1] ):

                click = event.get_pressed()

                # If click action exists and button is clicked
                if click[0] == 1:
                    if not self._pressed:
                        self.click()
                    self._pressed = True
                else:
                    self._pressed = False
                    # If mouse is over the button and is not clicked, do hover
                    self.hover()

            else:
                # Default action
                self.default()

            #display.blit(self, self._coords)
        else:
            # If disabled, don't show button
            self.set_alpha(0)

        # Blit the button using the super class's draw
        super(Button, self).draw(event, display)

    def default(self):
        # Default action
        try:
            self._default_action(self._default_args)
        except AttributeError:
            pass

    def click(self):
        try:
            self._click_action(self._click_args)
        except AttributeError:
            # If click isn't defined, hover
            self.hover()

    def hover(self):
        try:
            self._hover_action(self._hover_args)
        except AttributeError:
            # If hovering is not defined, do default
            self.default()

    def set_on_hover_action(self, function, args):
        """Accept a function to be executed when mouse hovers over button."""
        self._hover_action = function
        self._hover_args = args

    def set_on_click(self, function, args):
        """Accept a function to be executed when button is clicked."""
        self._click_action = function
        self._click_args = args

    def set_default_action(self, function, args):
        """Accept a function to be executed when button is clicked."""
        self._default_action = function
        self._default_args = args

    def set_enabled(self, enabled):
        """Set the button's enabled state."""
        self._is_enabled = enabled

    def is_enabled(self):
        """Get the button's enabled state."""
        return self._is_enabled
