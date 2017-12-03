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
                print("default")

                # hover action
                self.on_hover()

                # If click action exists and button is clicked
                if click[0] == 1:
                    self.on_click()
            else:
                # Non-hover action
                self.fill(pygame.Color(0,100,0))

            display.blit(self, self._coords)
        else:
            # Show disabled
            pass

        super(PyButton, self).draw(event, display)

    def on_hover(self):
        print("hover")
        self.fill(pygame.Color(200,0,0))

    def on_click(self):
        self.fill(pygame.Color(200,200,0))

    def set_enabled(self, enabled):
        self._is_enabled = enabled
