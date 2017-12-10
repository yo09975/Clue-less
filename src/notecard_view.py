"""notecard_view.py."""
from src.view import View
from src.button import Button
import pygame
from src.notecard_controller import NoteCardController
import time
from src.notecard import NoteCard

class NoteCardView(View):
    def __init__(self, x, y):
        super(NoteCardView, self).__init__(x, y, NoteCard.WIDTH * 30, NoteCard.HEIGHT * 30)
        self._note_card_controller = NoteCardController()
        self._nc = self._note_card_controller._note_card._note_state
        pygame.font.init()
        self._marks = [' ', 'Y', 'N', ' ?']
        self._font = pygame.font.SysFont('Comic Sans MS', 24)


        def mark(args):
            args['nc'].mark(args['x'], args['y'])

        for i in range(0, NoteCard.WIDTH):
            for j in range(0, NoteCard.HEIGHT):
                b = Button(i * 30 + self._coords[0], j * 30 + self._coords[1], 30, 30)
                b.set_alpha(0)
                b.set_on_click(mark, {'nc': self._note_card_controller, 'x': int(i), 'y': int(j)})
                self.add_view(b)


    def draw(self, event, display):
        super(NoteCardView, self).draw(event, display)

        for i in range(0, NoteCard.WIDTH):
            for j in range(0, NoteCard.HEIGHT):
                mark = self._marks[self._nc[i][j]]
                if mark == 0:
                    next
                sur = self._font.render(mark, False, (0, 0, 0))
                display.blit(sur, (i * 30 + self._coords[0] + 4, j * 30 + self._coords[1] - 4))
