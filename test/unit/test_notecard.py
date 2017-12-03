"""test_notecard.py

Ensure that the notecard is properly iterating through note states.
"""
from src.notecard import NoteCard
from src.notecard_controller import NoteCardController as NCC

def test_mark():
    ncc = NCC()
    assert ncc._note_card._note_state[1][1] == 0
    ncc.mark(1, 1)
    assert ncc._note_card._note_state[1][1] == 1
    ncc.mark(1, 1)
    ncc.mark(1, 1)
    ncc.mark(1, 1)
    assert ncc._note_card._note_state[1][1] == 0


def test_out_of_range():
    ncc = NCC()
    ncc.mark(-1, 0)
    ncc.mark(0, -1)
    ncc.mark(6, 0)
    ncc.mark(0, 21)
