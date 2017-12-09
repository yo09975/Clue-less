#!/usr/bin/env python3.6

"""gamecontroller.py."""
from src.gamestate import GameState
from src.suggestion_engine import SuggestionEngine
from src.movementengine import MovementEngine
from src.network.message import Message
from src.network.message import MessageType
from src.gamestatus import GameStatus
from src.move import Move
from src.suggestion import Suggestion
from src.playerlist import PlayerList
from src.network.servernetworkinterface import ServerNetworkInterface
from src.player import Player
from src.playerstatus import PlayerStatus
from src.board import Board
import json


class GameController(object):
    """Overall controller of a game used to update Game State.

    GameController class in the Game Management Subsystem.  Takes inputs and
    outputs from other controllers and updates the GameState.  The central
    piece is a finite state machine, which has all of the game workflow built

    Attributes:
    _current_game - Instance of GameState object representing the current game
    _suggest_engine - Instance of SuggestionEngine object for processing
                     suggestions
    _move_engine - Instance of MovementEngine object for processing moves

    """

    def __init__(self):
        """Constructor"""
        print('Constructor in GameController class')
        self._current_game = GameState()
        self._suggest_engine = SuggestionEngine(self._current_game)
        self._move_engine = MovementEngine()

    def get_game_state(self) -> GameState:
        """Returns GameState reference"""
        return self._current_game

    def get_suggest_engine(self) -> SuggestionEngine:
        """Returns SuggestionEngine reference"""
        return self._suggest_engine

    def get_move_engine(self) -> MovementEngine:
        """Returns MovementEngine reference"""
        return self._move_engine

    def start(self):
        """Accepts a Message to process"""

        sni = ServerNetworkInterface()
        sni.start()

        while(True):

            message = sni.get_message()

            if not message:
                continue

            if message is not None:
                """Tear apart message"""
                msg_uuid = message.get_uuid()
                msg_type = message.get_msg_type()
                msg_payload = message.get_payload()
                """Retrieve current game status for comparisons"""
                state = self._current_game.get_state()

                pl = PlayerList()

                """Short circuits any additional processing if a player leaves the
                   game
                """
                if msg_type == MessageType.LEAVE_GAME:
                    leaving_player = get_player_from_uuid(msg_uuid)
                    leaving_player_character = leaving_player.get_character(
                        ).get_id()
                    leave_message = Message(sni.get_uuid(
                        ), MessageType.NOTIFY, f'{leaving_player_character} \
                        has left the game.')
                    sni.send_all(leave_message)
                    self._current_game.set_state(GameStatus.LOBBY)

                else:

                    # Initial game setup where players are choosing their characters
                    if state == GameStatus.LOBBY:

                        if msg_type == MessageType.SELECT_PIECE:
                            card_id = msg_payload
                            selected_player = pl.get_player(card_id)
                            if selected_player.get_uuid() is None:
                                selected_player.set_uuid(msg_uuid)
                                selected_player.set_status(PlayerStatus.ACTIVE)
                            update_message = Message(sni.get_uuid(
                                ), MessageType.SEND_PLAYERS, pl.serialize())
                            sni.send_all(update_message)

                        if msg_type == MessageType.START_GAME:
                            total_players = 0
                            for p in pl.get_players():
                                if p.get_status() == PlayerStatus.ACTIVE:
                                    total_players += 1
                            if total_players >= 2:
                                self._current_game.start()
                                # Get first player
                                first_player = pl.get_player_by_index(self._current_game.get_current_player())

                                # Tell all player's whose turn it is
                                notify_msg = Message(sni.get_uuid(), MessageType.NOTIFY,
                                    f'Currently taking their turn: {first_player.get_character()}')
                                sni.send_all(notify_msg)

                                # Notify player it's their turn
                                your_turn_payload = json.dumps({ 'was_transferred': first_player.get_was_transferred() })
                                your_turn_msg = Message(sni.get_uuid(), MessageType.YOUR_TURN, your_turn_payload)
                                sni.send_message(first_player.get_uuid(), your_turn_msg)

                                # Change GameStatus
                                self._current_game.set_state(GameStatus.START_TURN)

                    # Start of a turn, player can Move, Suggestion, Accuse, or End Turn
                    elif state == GameStatus.START_TURN:

                        if msg_type == MessageType.MOVEMENT:
                            move = Move.deserialize(msg_payload)
                            if self._move_engine.is_valid_move(move):
                                self._move_engine.do_move(move)
                                moving_player = self.get_player_from_uuid(msg_uuid)
                                moving_player.set_was_transferred(False)
                                self._current_game.set_state(GameStatus.POST_MOVE)
                                update_board_message = Message(
                                    sni.get_uuid(), MessageType.UPDATE_BOARD,
                                    self._move_engine._board.serialize())
                                sni.send_all(update_board_message)

                        elif msg_type == MessageType.SUGGESTION_MAKE:
                            suggesting_player = self.get_player_from_uuid(msg_uuid)
                            if suggesting_player.get_was_transferred():
                                self.do_suggestion(
                                    msg_uuid, msg_type, msg_payload, suggesting_player)

                        elif msg_type == MessageType.ACCUSATION:
                            self.do_accusation(msg_uuid, msg_type, msg_payload)

                        elif msg_type == MessageType.END_TURN:
                            self.do_end_turn()

                    # After a move, player can Suggestion, Accuse, or End Turn
                    elif state == GameStatus.POST_MOVE:

                        if msg_type == MessageType.SUGGESTION_MAKE:
                            suggesting_player = self.get_player_from_uuid(msg_uuid)
                            self.do_suggestion(
                                msg_uuid, msg_type, msg_payload, suggesting_player)

                        elif msg_type == MessageType.ACCUSATION:
                            self.do_accusation(msg_uuid, msg_type, msg_payload)

                        elif msg_type == MessageType.END_TURN:
                            self.do_end_turn()

                    # After suggestion is made, waiting for suggestion response
                    elif state == GameStatus.WAIT_SUGG:

                        if msg_type == MessageType.SUGGESTION_RESPONSE:
                            card = Card.deserialize(payload)
                            self._suggest_engine.answer_suggestion(card)
                            self._current_game.set_state(GameStatus.POST_SUGG)

                    # After a suggestion is answered, player can Accuse, or End Turn
                    elif state == GameStatus.POST_SUGG:

                        if msg_type == MessageType.ACCUSATION:
                            self.do_accusation(msg_uuid, msg_type, msg_payload)

                        elif msg_type == MessageType.END_TURN:
                            self.do_end_turn()

    def get_player_from_uuid(msg_uuid: str) -> Player:
        players = pl.get_players()
        for p in players:
            if msg_uuid == p.get_uuid():
                return p

    def do_suggestion(
        msg_uuid: str, msg_type: MessageType, msg_payload: str,
            suggesting_player: Player):
        suggestion = Suggestion.deserialize(msg_payload)
        if self._suggest_engine.is_valid_suggestion(
                suggesting_player, suggestion):
            if self._suggest_engine.make_suggestion(suggestion):
                self._current_game.set_state(GameStatus.WAIT_SUGG)
            else:
                self._current_game.set_state(GameStatus.POST_SUGG)
            suggested_player = pl.get_player(
                suggestion.get_character().get_id())
            suggested_location = suggestion.get_room().get_id()
            self._move_engine.do_move(Move(
                suggested_player.get_card_id(), suggested_location))
            suggested_player.set_was_transferred(True)
            suggesting_player.set_was_transferred(False)
            update_board_message = Message(
                sni.get_uuid(), MessageType.UPDATE_BOARD,
                self._move_engine._board.serialize())
            sni.send_all(update_board_message)

    def do_accusation(msg_uuid: str, msg_type: MessageType, msg_payload: str):
        accusation = Suggestion.deserialize(msg_payload)
        players = pl.get_players()
        accuser = players[self._current_game.get_current_player()]
        if self._suggest_engine.make_accusation(accusation, accuser):
            self._current_game.set_state(GameStatus.LOBBY)
        else:
            accuser.set_status(PlayerStatus.LOST)
            next_player = self._current_game.next_turn()
            # Check to see if everyone has lost
            if next_player is None:
                all_lost_message = Message(
                    sni.get_uuid(), MessageType.NOTIFY, 'All players have made \
                    an incorrect accusation. No one wins.')
                self._current_game.set_state(GameStatus.LOBBY)
            else:
                self.do_end_turn()

    def do_end_turn(msg_uuid: str, msg_type: MessageType, msg_payload: str):
        # Changes GameState's _current_player
        self._current_game.next_turn()
        next_player = pl.get_player_by_index(self._current_game.get_current_player())

        # Tell all player's whose turn it is
        notify_msg = Message(sni.get_uuid(), MessageType.NOTIFY,
            f'Currently taking their turn: {next_player.get_character()}')
        sni.send_all(notify_msg)

        # Notify player it's their turn
        your_turn_payload = json.dumps({ 'was_transferred': next_player.get_was_transferred() })
        your_turn_msg = Message(sni.get_uuid(), MessageType.YOUR_TURN, your_turn_payload)
        sni.send_message(next_player.get_uuid(), your_turn_msg)

        # Change GameStatus
        self._current_game.set_state(GameStatus.START_TURN)

if __name__ == '__main__':
    try:
        gc = GameController()
        gc.start()
    except KeyboardInterrupt:
        print('Interrupted')
        exit(0)

