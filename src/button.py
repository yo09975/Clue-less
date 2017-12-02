"""button.py"""
import pygame

class Button(pygame.Surface):
    """
    A rectangular region that performs certain actions if hovered over or clicked.
    Can be invisible, have a color background, or have a picture background.  Can be disabled.
    """

    click_action = None  # method object to be executed when the parent Button object is clicked
    hover_action = None  # method object to be executed when the parent Button object is hovered over
    is_enabled = None    # Boolean representing if the Button object is currently enabled

    def set_xy(self, rect):
        self._rect = rect

    def draw(self, display, event):

        mouse = event.get_pos()
        self._is_enabled = True
        if (self._is_enabled):
            # If mouse is over button, process clicks and hoveraction
            if (self._rect[0] < mouse[0] < self._rect[0] + self.get_size()[0] and self._rect[1] < mouse[1] < self._rect[1] + self.get_size()[1] ):
                click = event.get_pressed()

                # hover action
                self.fill(pygame.Color(200,0,0))

                # If click action exists and button is clicked
                if click[0] == 1:
                    print("clicked!")
            else:
                # Non-hover action
                self.fill(pygame.Color(0,0,0))

            display.blit(self, self._rect)
        else:
            # Show disabled

        #if mouse[0] && mouse [y]

    def set_click_action(self, click_action):
        """Accepts a method to set what is executed when Button is clicked"""
        return True

    def set_hover_action(self, hover_action):
        """Accepts a method to set what is executed when Button is hovered over"""
        return True

    def set_enabled(self, is_enabled):
        """Accepts a Boolean to set whether a Button is enabled or not"""
        return True
