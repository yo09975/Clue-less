"""NoteCardView.py"""


class NoteCardView(object):
    """
    Rendering a Matrix of Buttons that helps the user make logical deductions about
    which cards might or might not be the guilty party
    """

    current_notes = None    # two-dimensional array of Button objects that represents a note card
    note_card = None    # NoteCard object to be displayed

    def __init__(self, note_card):
        """Constructor that accepts a NoteCard object"""
        self.__note_card = note_card

    def update(self):
        """Updates the current_notes attribute"""
        return True
