"""suggestion_engine.py"""

from src.suggestion import Suggestion
from src.gamestate import GameState
from src.cardtype import CardType
from src.playerlist import PlayerList
from src.player import Player


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
    and all other opponents are notified that the suggestion was incorrect.
    In the case where the suggestion is correct, the Suggestion Engine
    notifies all Players that a correct suggestion has been made.

    """

    def __init__(self, game_state: GameState):
        """Constructor. Utilizes the GameState"""

        self.game_state = game_state

    def make_suggestion(self, suggestion: Suggestion):
        """Makes a suggestion. Also offers to move the suggested character to the suggested room."""

        responder = self.game_state.next_turn()  # The first person to "answer" is the next player.

        if (suggestion.get_room().get_type() != CardType.ROOM) or (suggestion.get_weapon().get_type() != CardType.WEAPON) or (suggestion.get_character().get_type() != CardType.SUSPECT):
            print('This is not a valid suggestion. It requires a room, weapon, and character.')  # placeholder message
        else:
            # send message to MovementEngine to move character
            while responder != self.game_state.get_current_player():
                response = self.answer_suggestion(suggestion, responder)
                if response in suggestion.get_suggestion_set():
                    print("A suggestion was refuted.")  # placeholder message
                    return False
                else:
                    responder = PlayerList.get_next_player(responder)
            print("The suggestion could not be refuted.")  # placeholder message
            return True

    def answer_suggestion(self, suggestion: Suggestion, responder: Player):
        """Allows a player to answer a suggestion."""

        print(suggestion)
        response = input('Pick a from your hand that will refute the suggestion, if possible. If not enter None.')
        if response in responder.get_hand() and response in suggestion.get_suggestion_set():
            return response
        else:
            return 'None'

    def make_accusation(self, suggestion: Suggestion, accuser: Player):
        """Makes an accusation; if correct the game is won, if not the player loses."""

        if suggestion == self.game_state.get_solution():
            self.game_state.set_status("WON")
        else:
            accuser.set_status(3)
