"""suggestion_engine.py"""

from src.suggestion import Suggestion
from src.gamestate import GameState
from src.card import Card
from src.cardtype import CardType
from src.playerlist import PlayerList
from src.player import Player
from src.playerstatus import PlayerStatus
from src.network.message import Message, MessageType
from src.network.servernetworkinterface import ServerNetworkInterface as SNI
from src.location import Location
import json

class SuggestionEngine:
    """Make Suggestion is responsible for taking Player input of character,
    weapon, and room. Error Checking ensures an invalid suggestion cannot
    be made. Make Suggestion also provides input to the Movement Engine to
    move a suggested Character to the suggested Room. Answer Suggestion
    takes input from Make Suggestion and displays them to the Opponents.
    In sequence, Opponent may select one card that is capable of disproving
    the suggestion. This sequence ends when the first disproving answer is
    provided. Opponents will be unable to play any cards that don’t disprove
    the suggestion. The disproving card is shown to the Suggesting Player,
    and all other opponents are notified that the suggestion was incorrect.
    In the case where the suggestion is correct, the Suggestion Engine
    notifies all Players that a correct suggestion has been made.

    """

    def __init__(self, game_state: GameState):
        """Constructor. Utilizes the GameState"""

        self.game_state = game_state

    def make_suggestion(self, suggestion: Suggestion):
        """Makes a suggestion. Also offers to move the suggested character to the suggested room."""
        """These are some acrobatics to initialize the suggesting player and responding player."""
        sni = SNI()
        pl = PlayerList()
        current = self.game_state.get_current_player()
        players = pl.get_players()
        suggesting_player = players[current]
        responder = pl.get_next_player(suggesting_player)

        """Iterating through each player in PlayerList. If they are able to refute, we send a SUGGESTION_REQUEST to
        them asking that they select a card with which to refute the suggestion. If a player cannot refute we let
        all users know they were unable to refute."""

        # Put this into a dict because it doesn't deserialize into just a Suggestion
        sugg_msg = {}
        sugg_msg['suggester'] = suggesting_player.get_character().get_id()
        sugg_msg['suggestion'] = suggestion.serialize()

        suggestion_msg = Message(sni.get_uuid(), MessageType.SUGGESTION_NOTIFY,
                                 json.dumps(sugg_msg))
        sni.send_all(suggestion_msg)

        while responder != suggesting_player:
            hand = responder.get_hand()
            if hand.contains_card(suggestion.get_room()) or hand.contains_card(suggestion.get_character()) or \
                    hand.contains_card(suggestion.get_weapon()):
                request_msg = Message(sni.get_uuid(), MessageType.SUGGESTION_REQUEST,
                                       suggestion.serialize())
                sni.send_message(responder.get_uuid(), request_msg)

                # Send a SUGGESTION_OUTCOME to everyone when suggestion is disproved
                response_notification = Message(sni.get_uuid(),
                                        MessageType.SUGGESTION_OUTCOME,
                                        responder.get_character().get_id() + \
                                        " will disprove the suggestion.")
                sni.send_all(response_notification)
                return True
            else:
                # Send a SUGGESTION_OUTCOME message to everyone when a
                # suggestion cannot be disproved
                could_not_respond_msg = Message(sni.get_uuid(),
                                        MessageType.SUGGESTION_OUTCOME,
                                        responder.get_character().get_id() + \
                                        " could not disprove the suggestion.")
                sni.send_all(could_not_respond_msg)
                responder = pl.get_next_player(responder)

        # Send a SUGGESTION_NO_REFUTE to suggester if no one can disprove.
        no_response_to_suggester = Message(sni.get_uuid(), MessageType.SUGGESTION_NO_REFUTE, "")
        sni.send_message(suggesting_player.get_uuid(), no_response_to_suggester)

        # Send a SUGGESTION_OUTCOME if none of the players can disprove the suggestion
        no_response_msg = Message(sni.get_uuid(),
                          MessageType.SUGGESTION_OUTCOME,
                          "The suggestion could not be disproved.")
        sni.send_all(no_response_msg)





        return False

    def answer_suggestion(self, response: Card):
        """Allows a player to answer a suggestion."""
        sni = SNI()
        pl = PlayerList()
        current = self.game_state.get_current_player()
        players = pl.get_players()
        suggesting_player = players[current]
        response_msg = Message(sni.get_uuid(), MessageType.SUGGESTION_RESPONSE, response.serialize())
        sni.send_message(suggesting_player.get_uuid(), response_msg)

    def make_accusation(self, suggestion: Suggestion, accuser: Player):
        """Makes an accusation; if correct the game is won, if not the player loses and everyone is notified."""

        sni = SNI()
        if suggestion == self.game_state.get_solution():
            correct_accusation_msg = Message(sni.get_uuid(), MessageType.ACCUSATION_NOTIFY,
                                     suggestion.serialize())
            sni.send_all(correct_accusation_msg)
            correct_notification_msg = Message(sni.get_uuid(), MessageType.NOTIFY,
                                       accuser.get_character().get_id() + " made a correct accusation.")
            sni.send_all(correct_notification_msg)
            return True
        else:
            accuser.set_status(PlayerStatus.LOST)
            accusation_msg = Message(sni.get_uuid(), MessageType.ACCUSATION_NOTIFY,
                                     suggestion.serialize())
            sni.send_all(accusation_msg)
            notification_msg = Message(sni.get_uuid(), MessageType.NOTIFY,
                                       accuser.get_character().get_id() + " made an incorrect accusation.")
            sni.send_all(notification_msg)
            return False

    def is_valid_suggestion(self, player_location: Location, suggestion: Suggestion) -> bool:
        """Makes sure the suggesting player is in the room suggested"""
        return player_location.get_name() == suggestion.get_room().get_id()
