import sys, os
import pygame

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from src.view import View
from src.suggestion_dialog import SuggestionDialog as SD
from src.answer_suggestion_dialog import AnswerSuggestionDialog as ASD
from src.character_picker_dialog import CharacterPickerDialog as CPD
from src.notecard_view import NoteCardView
from src.button import Button
from enum import Enum
from src.playerstate import PlayerState
import json
from queue import Queue
from threading import Thread
from src.network.message import MessageType
from src.network.message import Message
from src.network.clientnetworkinterface import ClientNetworkInterface as CNI
from src.playerlist import PlayerList
from src.board import Board
from src.move import Move
import time


class GameApp:
    def __init__(self):

        pygame.init()

        self._state = PlayerState.SELECT_PLAYER

        self._gameDisplay = pygame.display.set_mode((1410, 900))
        self._crashed = False


        self._background = pygame.image.load('resources/gameplaygui.jpg')

        # Set up different views

        # Set up Suggestion Dialog
        def send_suggestion(args):
            sugg_dialog = args['d']
            sugg = sugg_dialog.get_suggestion()
            if sugg is not None:
                sugg_dialog.set_is_visible(False)
                sugg_dialog.set_success(True)
                cni = CNI()
                message = Message(cni.get_uuid(), args['mt'], sugg.serialize())
                cni.send(message)

        self._sugg_dialog = SD(60, 60)
        self._sugg_dialog.set_is_visible(False)
        self._sugg_dialog.get_top_button().set_on_click(send_suggestion, {'d': self._sugg_dialog, 'mt': MessageType.SUGGESTION_MAKE})

        # Set up Accusation Dialog
        self._acc_dialog = SD(60, 60)
        self._acc_dialog.set_is_visible(False)
        self._sugg_dialog.get_top_button().set_on_click(send_suggestion, {'d': self._sugg_dialog, 'mt': MessageType.ACCUSATION})


        # Set up Suggestion Response Dialog
        self._ans_sugg_dialog = ASD(60, 60)
        self._ans_sugg_dialog.set_is_visible(False)


        # Set up character picker dialog
        self._char_picker_dialog = CPD(80, 80)
        self._char_picker_dialog.set_is_visible(True)



        # Set up board
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, '../data/locations.json')

        with open(filename) as data_file:
            locs = json.load(data_file)

        self._disp_board = {}
        ref_board = {}

        for l in locs['locations']:
            def location_hover(args):
                args['b'].fill(pygame.Color(255, 0, 0))
                args['b'].set_alpha(100)

            def location_click(args):
                cni = CNI()
                move = Move(cni.get_uuid(), args['loc_id'])
                message = Message(cni.get_uuid(), MessageType.MOVEMENT, move.serialize())
                cni.send_message(message)
                args['s'] = PlayerState.POST_MOVE

            location = Button(l['dims']['x'], l['dims']['y'], l['dims']['width'], l['dims']['height'])
            location.set_on_click(location_click, {'loc_id': l['key'], 's': self._state})
            # location.set_on_hover_action(location_hover, {'b': location})

            ref_board[l['key']] = location
            self._disp_board[l['key']] = location
            if l['type'] == "room":
                ref_board[l['name']] = location

        # Set up note card
        self._note_card = NoteCardView(1231, 121)

        # Set up make suggestion button
        self._make_sugg_button = Button(1056, 756, 170, 65)

        def make_suggestion(args):
            args['d'].set_is_visible(True)

        self._make_sugg_button.set_on_click(make_suggestion, {'d': self._sugg_dialog})

        # Set up make accusation button
        self._make_acc_button = Button(1236, 756, 170, 65)

        def make_accusation(args):
            args['d'].set_is_visible(True)

        self._make_acc_button.set_on_click(make_accusation, {'d': self._acc_dialog})

        # Set up end turn button
        self._end_turn_button = Button(1056, 831, 170, 65)

        def end_turn(args):
            cni = CNI()
            message = Message(cni.get_uuid(), MessageType.END_TURN, "")
            cni.send_message(message)
            args['s'] = PlayerState.WAIT_FOR_TURN

        self._end_turn_button.set_on_click(end_turn, {'s': self._state})

        # Set up leave game button
        self._leave_game_button = Button(1236, 831, 170, 65)

        def end_turn(args):
            cni = CNI()
            message = Message(cni.get_uuid(), MessageType.END_TURN, "")
            cni.send_message(message)
            args['s'] = PlayerState.SELECT_PIECE

        self._leave_game_button.set_on_click(end_turn, {'s': self._state})

        self._state_change_button = Button(0, 0, 20, 20)

        def change_state(args):
            args['g']._state = PlayerState(args['g']._state.value + 1)
            print(str(args['g']._state))

        self._state_change_button.set_on_click(change_state, {'g': self})

    def start(self):

        clock = pygame.time.Clock()
        cni = CNI()
        # ENTER MAIN GAME LOOP
        while not self._crashed:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True

            # Get latest message, if any
            # message = Message("tes", MessageType.NOTIFY, "yes")
            message = cni.get_message()
            if message is not None:
                print('\nReceived msg:', message.get_msg_type())
            else:
                print('.', end='', flush=True)

            self._gameDisplay.blit(self._background, (0, 0))

            self._state_change_button.draw(pygame.mouse, self._gameDisplay)

            # Always draw note card and leave game
            self._note_card.draw(pygame.mouse, self._gameDisplay)
            self._leave_game_button.draw(pygame.mouse, self._gameDisplay)

            # Always draw game pieces on the game board
            # TODO render game pieces

            # Display views based on state
            if self._state == PlayerState.SELECT_PLAYER:
                if message is not None:
                    if message.get_msg_type() == MessageType.SEND_PLAYERS:
                        # Deserialize player list, find taken tokens, and hide
                        pl = PlayerList.deserialize(message.get_payload())
                        player_list = pl.get_players()
                        unavailable = []
                        for p in player_list:
                            if p.get_uuid() is not None and p.get_uuid() != cni.get_uuid():
                                unavailable.append(p)

                        self._char_picker_dialog.set_unavailable_players(unavailable)

                    elif message.get_msg_type() == MessageType.PLAYER_HAND:
                        # Start game
                        self._state = PlayerState.WAIT_FOR_TURN
                        self._hand = Hand.deserialize(message.get_payload())

                # Display player picker
                self._char_picker_dialog.draw(pygame.mouse, self._gameDisplay)

            elif self._state == PlayerState.WAIT_FOR_TURN:
                # Display suggestion, accusation, board, and next turn butotns
                if message is not None:
                    if message.get_msg_type() == MessageType.SUGGESTION_REQUEST:
                        self._state = PlayerState.ANSWER_SUGGESTION

                        # Show answer suggestion dialog and disable any NA cards
                        self._ans_sugg_dialog.set_is_visible(True)
                        suggestion = Suggestion.deserialize(message.get_payload())
                        self._ans_sugg_dialog.set_suggestion(suggestion)
                        self._ans_sugg_dialog.set_player_hand(self._hand)

                    elif message.get_msg_type() == MessageType.UPDATE_BOARD:
                        # Update board
                        self._board = Board.deserialize(message.get_payload())

                    elif message.get_msg_type() == MessageType.YOUR_TURN:
                        # Make it your turn
                        self._state = PlayerState.MY_TURN


            elif self._state == PlayerState.ANSWER_SUGGESTION:
                self._ans_sugg_dialog.draw(pygame.mouse, self._gameDisplay)
                # Wait for button action to change game state
                if self._ans_sugg_dialog.get_success():
                    self._state = PlayerState.WAIT_FOR_TURN

            elif self._state == PlayerState.MY_TURN:
                # Wait for button action to change game state
                if self._acc_dialog.get_success():
                    self._state = PlayerState.WAIT_FOR_TURN
                elif self._sugg_dialog.get_success():
                    self._state = PlayerState.POST_SUGGESTION

                # Buttons
                self._make_acc_button.draw(pygame.mouse, self._gameDisplay)
                self._make_sugg_button.draw(pygame.mouse, self._gameDisplay)
                self._end_turn_button.draw(pygame.mouse, self._gameDisplay)

                for l in self._disp_board:
                    self._disp_board[l].draw(pygame.mouse, self._gameDisplay)

                # Dialogs
                self._sugg_dialog.draw(pygame.mouse, self._gameDisplay)
                self._acc_dialog.draw(pygame.mouse, self._gameDisplay)

            elif self._state == PlayerState.POST_SUGGESTION:
                if message is not None:
                    if message.get_msg_type() == MessageType.SUGGESTION_NOTIFY:
                        # TODO Write suggestion notification to msg center
                        self._state = PlayerState.POST_SUGGESTION_ANSWER

                    elif message.get_msg_type() == MessageType.UPDATE_BOARD:
                        # Update board
                        self._board = Board.deserialize(message.get_payload())


            elif self._state == PlayerState.POST_SUGGESTION_ANSWER:
                # Wait for button actions to change state
                if self._acc_dialog.get_success():
                    self._state = PlayerState.WAIT_FOR_TURN

                # Buttons
                self._make_acc_button.draw(pygame.mouse, self._gameDisplay)
                self._end_turn_button.draw(pygame.mouse, self._gameDisplay)

                # Dialogs
                self._sugg_dialog.draw(pygame.mouse, self._gameDisplay)
                self._acc_dialog.draw(pygame.mouse, self._gameDisplay)


            elif self._state == PlayerState.POST_MOVE:
                # Wait for button actions to change state
                if self._acc_dialog.get_success():
                    self._state = PlayerState.WAIT_FOR_TURN
                elif self._sugg_dialog.get_success():
                    self._state = PlayerState.POST_SUGGESTION

                # Buttons
                self._make_acc_button.draw(pygame.mouse, self._gameDisplay)
                self._make_sugg_button.draw(pygame.mouse, self._gameDisplay)
                self._end_turn_button.draw(pygame.mouse, self._gameDisplay)

                # Dialogs
                self._sugg_dialog.draw(pygame.mouse, self._gameDisplay)
                self._acc_dialog.draw(pygame.mouse, self._gameDisplay)
            elif message is not None:
                if message.get_msg_type() == MessageType.NOTIFY:
                    # TODO update notification center
                    pass

            pygame.display.update()

            clock.tick(60)



cni = CNI()
cni.connect('localhost')
game = GameApp()
game.start()
