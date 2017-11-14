class SuggestionEngine:
	"""Make Suggestion is responsible for taking Player input of character,
	weapon, and room. Error Checking ensures an invalid suggestion cannot 
	be made. Make Suggestion also provides input to the Movement Engine to
	 move a suggested Character to the suggested Room. Answer Suggestion 
	 takes input from Make Suggestion and displays them to the Opponents. 
	 In sequence, Opponent may select one card that is capable of disproving
	 he suggestion. This sequence ends when the first disproving answer is 
	 provided. Opponents will be unable to play any cards that don’t disprove
	 he suggestion. The disproving card is shown to the Suggesting Player, 
	 and all other opponents are notified that the suggestion was disproven. 
	 n the case where the suggestion is correct, the Suggestion Engine 
	 notifies all Players that a correct suggestion has been made. """

	 _name = None

	 _game_state = None

	 def __init__(self, name: str, gamestate: GameState):
	 	self._name = name

	 	self._game_state = gamestate

	 def make_suggestion(self, suggestion: Suggestion):
	 	"""make a suggestion"""
	 	suggested_move = Move(suggestion.get_character(), suggestion.get_room)
	 	game_state.move_engine.do_move(suggested_move)

	 def answer_suggestion(self, suggestion: Suggestion):
	 	"""answer a suggestion"""
	 	return response_card

	 def make_accusation(self, suggestion: Suggestion, player_id: str):
	 	if suggestion == self._game_state.get_solution():
	 		self._game_state.set_state(won)
	 	else:
	 		player_id.set_status(inactive)
