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
from src.hand import Hand
from src.cardtype import CardType
from src.card import Card
from src.suggestion import Suggestion
import time


class GameApp:
    def __init__(self):

        pygame.init()

        self._state = PlayerState.SELECT_PLAYER

        self._gameDisplay = pygame.display.set_mode((1410, 900), pygame.RESIZABLE)
        icon = pygame.image.load('resources/bblogo.jpg')
        pygame.display.set_caption('Clue-Less by Blue Barracudas')
        pygame.display.set_icon(icon)
        self._crashed = False

        self._message_log = []

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
                cni.send_message(message)

        self._sugg_dialog = SD(60, 60)
        self._sugg_dialog.set_is_visible(False)
        self._sugg_dialog.get_top_button().set_on_click(send_suggestion, {'d': self._sugg_dialog, 'mt': MessageType.SUGGESTION_MAKE})

        # Set up Accusation Dialog
        self._acc_dialog = SD(60, 60)
        self._acc_dialog.set_is_visible(False)
        self._acc_dialog.get_top_button().set_on_click(send_suggestion, {'d': self._sugg_dialog, 'mt': MessageType.ACCUSATION})


        # Set up Suggestion Response Dialog
        self._ans_sugg_dialog = ASD(60, 60)
        self._ans_sugg_dialog.set_is_visible(False)


        # Set up character picker dialog
        self._char_picker_dialog = CPD(80, 80)
        self._char_picker_dialog.set_is_visible(True)


        # Set up board
        dir = os.path.dirname(__file__)
        location_file = os.path.join(dir, '../data/locations.json')

        with open(location_file) as data_file:
            locs = json.load(data_file)

        self._disp_board = {}
        self._ref_board = {}
        self._my_character = Card("placeholder", CardType.SUSPECT)
        # cross reference from card_id to avatar png

        self._player_hand_string = ""

        for l in locs['locations']:
            def location_hover(args):
                args['b'].fill(pygame.Color(255, 0, 0))
                args['b'].set_alpha(100)

            def location_click(args):

                args['s'] = PlayerState.POST_MOVE
                cni = CNI()
                move = Move(args['p'].get_character(), args['loc_id'])
                message = Message(cni.get_uuid(), MessageType.MOVEMENT, move.serialize())
                cni.send_message(message)

            location = Button(l['dims']['x'], l['dims']['y'], l['dims']['width'], l['dims']['height'])
            location.set_on_click(location_click, {'loc_id': l['key'], 's': self._state, 'p': self._char_picker_dialog})
            # location.set_on_hover_action(location_hover, {'b': location})
            self._ref_board[l['key']] = location
            self._disp_board[l['key']] = {}
            self._disp_board[l['key']]['button'] = location
            print("x")

            self._disp_board[l['key']]['x'] = l['dims']['x']
            print("y")

            self._disp_board[l['key']]['y'] = l['dims']['y']

            if l['type'] == "room":
                self._ref_board[l['name']] = location

        # Set up avatars
        card_file = os.path.join(dir, '../data/cards.json')

        with open(card_file) as data_file:
            cards = json.load(data_file)

        self._board = Board()

        # cross reference from card_id to avatar png
        self._avatars = {}
        # init board to set up PlayerList
        pl = PlayerList()
        pl.setup()
        for c in cards['cards']:
            if c['type'] == 'suspect':
                self._avatars[c['card_id']] = {}
                avatar = pygame.image.load('resources/' + c['avatar'])
                self._avatars[c['card_id']]['png'] = avatar
        self.determine_avatar_locations()

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
            args['s']._state = PlayerState.WAIT_FOR_TURN

        def leave_game(args):
            cni = CNI()
            message = Message(cni.get_uuid(), MessageType.LEAVE_GAME, "")
            cni.send_message(message)
            self._crashed = True

        self._end_turn_button.set_on_click(end_turn, {'s': self})

        # Set up leave game button
        self._leave_game_button = Button(1236, 831, 170, 65)

        def end_turn(args):
            cni = CNI()
            message = Message(cni.get_uuid(), MessageType.END_TURN, "")
            cni.send_message(message)
            args['s'] = PlayerState.SELECT_PIECE

        self._leave_game_button.set_on_click(leave_game, {'s': self._state})

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
                    self._crashed = True

            # Get latest message, if any
            message = cni.get_message()
            if message is not None:
                print(f'INCOMING: {message}')
                if message.get_msg_type() == MessageType.NOTIFY:
                    font = pygame.font.SysFont('Comic Sans MS', 16)
                    text_message = font.render(message.get_payload(), False, (0, 0, 0))
                    self._message_log.append(text_message)
                    # Keep last 5 messages
                    self._message_log = self._message_log[-4:]
                elif message.get_msg_type() == MessageType.PLAYER_HAND:
                    font = pygame.font.SysFont('Comic Sans MS', 16)
                    hand = Hand.deserialize(message.get_payload())
                    msg_string = "Your cards are "
                    for c in hand.get_cards():
                        msg_string +=  c.get_id() + ", "
                    self._player_hand_string = msg_string[:-2]
                elif message.get_msg_type() == MessageType.SUGGESTION_NOTIFY:
                    sugg = json.loads(message.get_payload())

                    font = pygame.font.SysFont('Comic Sans MS', 16)
                    msg_string = sugg['suggester'] + " suggests " + str(Suggestion.deserialize(sugg['suggestion']))
                    text_message = font.render(msg_string, False, (0, 0, 0))
                    self._message_log.append(text_message)
                    # Keep last 5 messages
                    self._message_log = self._message_log[-4:]


            else:
                print('.', end='', flush=True)

            self._gameDisplay.blit(self._background, (0, 0))

            self._state_change_button.draw(pygame.mouse, self._gameDisplay)

            # Always draw note card and leave game
            self._note_card.draw(pygame.mouse, self._gameDisplay)
            self._leave_game_button.draw(pygame.mouse, self._gameDisplay)

            # Always draw game pieces on the game board
            for a in self._avatars:
                self._gameDisplay.blit(self._avatars[a]['png'], (self._avatars[a]['x'], self._avatars[a]['y']))

            # Always render message log
            for i, text_message in enumerate(self._message_log):
                self._gameDisplay.blit(text_message, (20, 795 + 20 * i))

            # Always render hand
            disp_hand = font.render(self._player_hand_string, False, (0, 0, 0))
            self._gameDisplay.blit(text_message, (20, 775))

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

                        player_count = 0

                        for p in player_list:
                            if p.get_uuid() is not None:
                                player_count += 1

                        self._char_picker_dialog.get_bottom_button().set_enabled(player_count >= 2)

                    elif message.get_msg_type() == MessageType.PLAYER_HAND:
                        # Start game
                        self._state = PlayerState.WAIT_FOR_TURN
                        self._hand = Hand.deserialize(message.get_payload())
                        print("get char", self._char_picker_dialog.get_character())
                        self._my_character = self._char_picker_dialog.get_character()

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
                        print("Update board: ", message, message.get_payload())
                        self._board = self._board.deserialize(message.get_payload())
                        self.determine_avatar_locations()
                    elif message.get_msg_type() == MessageType.YOUR_TURN:
                        # Make it your turn
                        self._state = PlayerState.MY_TURN
                    elif message.get_msg_type() == MessageType.SUGGESTION_OUTCOME:
                        print(f'DEBUG: WAIT_FOR_TURN SUGGESTION_OUTCOME')
                        outcome = message.get_payload()
                        font = pygame.font.SysFont('Comic Sans MS', 16)
                        msg_string = outcome
                        text_message = font.render(msg_string, False, (0, 0, 0))
                        self._message_log.append(text_message)
                        # Keep last 5 messages
                        self._message_log = self._message_log[-5:]

            elif self._state == PlayerState.ANSWER_SUGGESTION:
                self._ans_sugg_dialog.draw(pygame.mouse, self._gameDisplay)

                if message is not None:

                    if message.get_msg_type() == MessageType.UPDATE_BOARD:
                        print(f'DEBUG: ANSWER_SUGGESTION UPDATE_BOARD')
                        # Update board
                        self._board = self._board.deserialize(message.get_payload())
                        self.determine_avatar_locations()


                # Wait for button action to change game state
                if self._ans_sugg_dialog.get_success():
                    self._state = PlayerState.WAIT_FOR_TURN

            elif self._state == PlayerState.MY_TURN:
                if message is not None:
                    if message.get_msg_type() == MessageType.UPDATE_BOARD:
                        # Update board
                        self._board = self._board.deserialize(message.get_payload())
                        self.determine_avatar_locations()
                        self._state = PlayerState.POST_MOVE

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
                    self._disp_board[l]['button'].draw(pygame.mouse, self._gameDisplay)

                # Dialogs
                self._sugg_dialog.draw(pygame.mouse, self._gameDisplay)
                self._acc_dialog.draw(pygame.mouse, self._gameDisplay)

            elif self._state == PlayerState.POST_SUGGESTION:
                if message is not None:
                    if message.get_msg_type() == MessageType.SUGGESTION_RESPONSE:
                        print(f'DEBUG: POST_SUGG SUGG_RESPONSE')
                        response = message.get_payload()
                        card = Card.deserialize(response)
                        font = pygame.font.SysFont('Comic Sans MS', 16)
                        msg_string = f'Your opponent disproved with {str(card)}'
                        text_message = font.render(msg_string, False, (0, 0, 0))
                        self._message_log.append(text_message)
                        # Keep last 5 messages
                        self._message_log = self._message_log[-5:]
                        # got the answer, move on!
                        self._state = PlayerState.POST_SUGGESTION_ANSWER

                    elif message.get_msg_type() == MessageType.SUGGESTION_OUTCOME:
                        print(f'DEBUG: POST SUGG SUGGESTION_OUTCOME')
                        outcome = message.get_payload()
                        font = pygame.font.SysFont('Comic Sans MS', 16)
                        msg_string = outcome
                        text_message = font.render(msg_string, False, (0, 0, 0))
                        self._message_log.append(text_message)
                        # Keep last 5 messages
                        self._message_log = self._message_log[-5:]

                    elif message.get_msg_type() == MessageType.UPDATE_BOARD:
                        # Update board
                        self._board = self._board.deserialize(message.get_payload())
                        self.determine_avatar_locations()

            elif self._state == PlayerState.POST_SUGGESTION_ANSWER:
                if message is not None:
                    if message.get_msg_type() == MessageType.UPDATE_BOARD:
                        # After Suggester gets answer, board not updated?
                        print(f'DEBUG: POST_SUGG_ANS UPDATE BOARD')
                        self._board = self._board.deserialize(message.get_payload())
                        self.determine_avatar_locations()


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
                if message is not None:
                    if message.get_msg_type() == MessageType.UPDATE_BOARD:
                        # Update board
                        self._board = self._board.deserialize(message.get_payload())
                        self.determine_avatar_locations()
                    else:
                        print(f'DEBUG: NOT EXPECTED MSG TYPE: {message.get_msg_type()}')

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


    def determine_avatar_locations(self):
        room_occupants = {}

        # Cycle through player list and build reference of occupants per rooms
        pl = PlayerList()
        for p in pl.get_players():
            loc = p.get_current_location()
            if loc not in room_occupants:
                room_occupants[loc] = []

            room_occupants[loc].append(p.get_card_id())

        # Calculate avatar location
        for loc in room_occupants:
            coords = (self._disp_board[loc]['x'], self._disp_board[loc]['y'])
            for i, card_id in enumerate(room_occupants[loc]):
                self._avatars[card_id]['x'] = coords[0] + i % 3 * 52 + 10
                self._avatars[card_id]['y'] = coords[1] + int(i/3) * 52

        print(self._avatars)

cni = CNI()
if (cni.connect('104.236.203.126')):
    game = GameApp()
    game.start()
else:
    print('Client was unable to connect to server.')
