class NoteCard:
    """Contains an array of lists. Each list is mapped to the associated color
     of an opponent and contains a symbol for each suspect, weapon, and place;
     either an X, a ?, a ✓, or nothing. Has the ability to mark cards that were
     shown (or deduced)	which only requires changing the symbol in the associated
     list."""

    WIDTH = 6
    HEIGHT = 21

    def __init__(self):
        self._note_state = [[0 for x in range(NoteCard.WIDTH)] for y in range(NoteCard.HEIGHT)]

    def mark(self, x: int, y: int):
        if NoteCard.WIDTH > x >= 0 and NoteCard.HEIGHT > y >= 0:
            self._note_state[x][y] = (self._note_state[x][y] + 1) % 4
