from notecard import NoteCard

class NoteCardStub:
	"""Contains an array of lists. Each list is mapped to the associated color
	 of an opponent and contains a symbol for each suspect, weapon, and place; 
	 either an X, a ?, a ✓, or nothing. Has the ability to mark cards that were 
	 shown (or deduced)	which only requires changing the symbol in the associated
	 list."""


	 def __init__(self):

	 	self._note_state = [[]]

	 def mark(self, x: int, y: int, symbol: str):
	 	"""note_state[x][y] = (note_state[x][y] + 1) % NUMBER_OF_MARKS"""
	 	