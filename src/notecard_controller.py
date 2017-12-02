class NoteCardController:
    """Receives input from the User Interface subsystem and translates
    the request into the appropriate call to mark the Note Card instance,
    thus updating its internal state."""
    def __init__(self):
        self._note_card = {}

    def mark(self, x: int, y: int):
        notecard.mark(x, y)
