"""suggestion_engine.py"""

from src.suggestion import Suggestion
from src.gamestate import GameState
from src.card import Card
from src.cardtype import CardType
from src.playerlist import PlayerList
from src.player import Player
from src.playerstatus import PlayerStatus
from src.network.message import Message, MessageType
from src.network.servernetworkinterface import ServerNetworkInterface


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

        current = self.game_state.get_current_player()
        players = PlayerList.get_players()
        suggesting_player = players[current]
        responder = PlayerList.get_next_player(suggesting_player)

        """First checking if the suggestion is valid. If not, we return True as the suggestion is refuted."""
        if (suggestion.get_room().get_type() != CardType.ROOM) or \
                (suggestion.get_weapon().get_type() != CardType.WEAPON) or \
                (suggestion.get_character().get_type() != CardType.SUSPECT):
            return True
        else:
            """Iterating through each player in PlayerList. If they are able to refute, we send a SUGGESTION_REQUEST to
            them asking that they select a card with which to refute the suggestion. If a player cannot refute we let
            all users know they were unable to refute."""
            suggestion_msg = Message(ServerNetworkInterface.get_uuid(), MessageType.SUGGESTION_NOTIFY,
                                     suggesting_player.get_character().get_name() + suggestion.serialize())
            ServerNetworkInterface.send_all(suggestion_msg)

            while responder != suggesting_player:
                hand = responder.get_hand()
                if hand.contains_card(suggestion.get_room()) or hand.contains_card(suggestion.get_character()) or \
                        hand.contains_card(suggestion.get_weapon()):
                    response_msg = Message(ServerNetworkInterface.get_uuid(), MessageType.SUGGESTION_REQUEST,
                                           suggestion.serialize())
                    ServerNetworkInterface.send_message(responder.get_uuid(), response_msg)
                    response_notification = Message(ServerNetworkInterface.get_uuid(), MessageType.SUGGESTION_NOTIFY,
                                                    responder.get_character().get_name() + "disproved the suggestion.")
                    ServerNetworkInterface.send_all(response_notification)
                    return True
                else:
                    could_not_respond_msg = Message(ServerNetworkInterface.get_uuid(), MessageType.SUGGESTION_NOTIFY,
                                                    responder.get_character().get_name() + " could not disprove.")
                    ServerNetworkInterface.send_all(could_not_respond_msg)
                    responder = PlayerList.get_next_player(responder)

            no_response_msg = Message(ServerNetworkInterface.get_uuid(), MessageType.SUGGESTION_NOTIFY,
                                      "The suggestion could not be refuted.")
            ServerNetworkInterface.send_all(no_response_msg)
            return False

    def answer_suggestion(self, response: Card):
        """Allows a player to answer a suggestion."""

        current = self.game_state.get_current_player()
        players = PlayerList.get_players()
        suggesting_player = players[current]
        response_msg = Message(ServerNetworkInterface.get_uuid(), MessageType.SUGGESTION_NOTIFY, response.serialize())
        ServerNetworkInterface.send_message(suggesting_player.get_uuid(), response_msg)

    def make_accusation(self, suggestion: Suggestion, accuser: Player):
        """Makes an accusation; if correct the game is won, if not the player loses and everyone is notified."""

        if suggestion == self.game_state.get_solution():
            correct_accusation_msg = Message(ServerNetworkInterface.get_uuid(), MessageType.ACCUSATION_NOTIFY,
                                     suggestion.serialize())
            ServerNetworkInterface.send_all(correct_accusation_msg)
            correct_notification_msg = Message(ServerNetworkInterface.get_uuid(), MessageType.NOTIFY,
                                       accuser.get_character().get_name() + " made a correct accusation.")
            ServerNetworkInterface.send_all(correct_notification_msg)
            return True
        else:
            accuser.set_status(PlayerStatus.LOST)
            accusation_msg = Message(ServerNetworkInterface.get_uuid(), MessageType.ACCUSATION_NOTIFY,
                                     suggestion.serialize())
            ServerNetworkInterface.send_all(accusation_msg)
            notification_msg = Message(ServerNetworkInterface.get_uuid(), MessageType.NOTIFY,
                                       accuser.get_character().get_name() + " made an incorrect accusation.")
            ServerNetworkInterface.send_all(notification_msg)
            return False
