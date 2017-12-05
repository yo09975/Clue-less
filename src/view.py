"""view.py.

Create a View which can hold and pass input to those subviews.
"""

import pygame


class View(pygame.Surface):
    """Create a View which can hold and pass input to those subviews."""

    def __init__(self, x, y, w, h):
        # List of subviews
        self._views = []
        self._is_visible = True
        # Absolute coordinates of this View
        self._coords = (x, y)

        super(View, self).__init__((w, h))

    def add_view(self, view):
        """Add a subview to this view."""
        self._views.append(view)

    def draw(self, event, display):
        if (self._is_visible):
            """Render this view and all subviews, and process any input."""
            # Render
            display.blit(self, self._coords)
            # Pass input to subviews and render them
            for v in self._views:
                v.draw(event, display)

    def set_is_visible(self, is_visible):
        self._is_visible = is_visible
