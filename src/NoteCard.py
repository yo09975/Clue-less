class NoteCard:
	"""Contains an array of lists. Each list is mapped to the associated color
	 of an opponent and contains a symbol for each suspect, weapon, and place; 
	 either an X, a ?, a ✓, or nothing. Has the ability to mark cards that were 
	 shown (or deduced)	which only requires changing the symbol in the associated
	 list."""

		 _note_state = None

	 def __init__(self, name: str, ):
	 	self._name = name
	 	self._note_state = [[]]

	 def mark(self, x: int, y: int, symbol: str):
	 	self._note_state[x][y] = str
	 	