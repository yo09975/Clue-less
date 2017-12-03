from src.pyview import PyView
import pygame

class PyButton(PyView):
    def __init__(self, x, y, w, h):
        self._is_enabled = True
        super(PyButton, self).__init__(x, y, w, h)

    def draw(self, event, display):
        mouse = event.get_pos()
        if (self._is_enabled):
            # If mouse is over button, process clicks and hoveraction
            if (self._coords[0] < mouse[0] < self._coords[0] + self.get_size()[0] and self._coords[1] < mouse[1] < self._coords[1] + self.get_size()[1] ):
                click = event.get_pressed()

                # If click action exists and button is clicked
                if click[0] == 1:
                    # try:
                    self._click_action(self._click_args)
                    # except:
                    #     pass
                else:
                    try:
                        self._hover_action(self._hover_args)
                    except:
                        pass

            else:
                # Non-hover action
                self.fill(pygame.Color(0, 100, 0))

            display.blit(self, self._coords)
        else:
            # Show disabled
            pass

        super(PyButton, self).draw(event, display)

    def set_on_hover_action(self, function, args):
        self._hover_action = function
        self._hover_args = args

    def set_on_click(self, function, args):
        self._click_action = function
        self._click_args = args

    def set_enabled(self, enabled):
        self._is_enabled = enabled
