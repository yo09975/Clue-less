import pygame

class PyView(pygame.Surface):
    def __init__(self, x, y, w, h):
        self._views = []
        self._coords = (x, y)
        super(PyView, self).__init__((w, h))

    def add_view(self, view):
        self._views.append(view)

    def draw(self, event, display):
        display.blit(self, self._coords)
        for v in self._views:
            v.draw(event, display)
