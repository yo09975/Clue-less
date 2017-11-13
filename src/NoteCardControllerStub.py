class NoteCardController:
	"""Receives input from the User Interface subsystem and translates
	 the request into the appropriate call to mark the Note Card instance,
	  thus updating its internal state."""

	 _note_card = None

	 def __init__(self, name: str, notecard: NoteCard):
	  	self._name = name
	  	
	  	self._note_card = notecard

	 def mark(self, x: int, y: int, symbol: str):
	  	notecard.mark(x, y, symbol)