from suggestion import Suggestion

class SuggestionStub:
	"""The object containing all Cards that make up a Player’s suggestion for the turn."""


	def __init__(self, room: Card, weapon: Card, character: Card):

		self._suggestion_set = (room, weapon, character)

	def get_suggestion_set(self):
		return self._suggestion_set

	def get_room(self):
		return self._suggestion_set[0]

	def get_weapon(self):
		return self._suggestion_set[1]

	def get_character(self):
		return self._suggestion_set[2]
			