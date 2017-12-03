"""game_app.py"""
#import user_interface
import pygame
import sys
sys.path.append("..")
from src.gamestate import GameState
from src.notecard_controller import NoteCardController
from src.notecard import NoteCard
from src.user_interface import UserInterface
# from src.gamestatus import GameStatus
from src.pybutton import PyButton
# from src.note_card_view import NoteCardView
from src.suggestion_dialog import SuggestionDialog
import os
import json

clock = pygame.time.Clock()


class GameApp():
    """
    Triggered by controllers to update after a move or suggestion has been asked.
    Can also show new views due to user action (asking for a suggestion).  Extends UserInterface.


    note_card_view = None   # two-dimensional array of button objects representing the note card information
    note_card = None    # a reference to the current note_card
    note_card_controller = None    # a reference to the NoteCardController to send clicks
    """

    def __init__(self, interface: UserInterface, game_state: GameState, note_card: NoteCard, note_card_controller: NoteCardController):
        # self._game_state = game_state
        #
        # self.__note_card = note_card
        # self.__note_card_controller = note_card_controller

        pygame.init()
        gameDisplay = pygame.display.set_mode((1410, 900))
        crashed = False

        game_img = pygame.image.load('../data/clue-less_board.png')



        # Set up game board
        board = {}

        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, '../data/locations.json')

        with open(filename) as data_file:
            locs = json.load(data_file)

        for l in locs['locations']:
            def location_hover(args):
                args['b'].fill(pygame.Color(0, 0, 100))
                args['b'].set_alpha(100)

            def location_default(args):
                args['b'].set_alpha(0)

            location = PyButton(l['dims']['x'], l['dims']['y'], l['dims']['width'], l['dims']['height'])
            location.set_default_action(location_default, {'b': location})
            location.set_on_hover_action(location_hover, {'b': location})

            board[l['key']] = location
            if l['type'] == "room":
                board[l['name']] = location
            # TODO Need to assign click actions


        # Set up NoteCard
        #notecard_view = NoteCardView(self._note_card)

        # Always display the board and notecard
        # ENTER MAIN GAME LOOP
        while not crashed:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True

            gameDisplay.blit(game_img, (0, 0))

            for loc in board:
                board[loc].draw( pygame.mouse, gameDisplay)
            # notecard_view.draw(gameDisplay, pygame.mouse)

            # # Detect state and draw accordingly
            # if self._game_state.get_state() == GameStatus.LOBBY:
            #     # pick_players.draw(gameDisplay, pygame.mouse)
            #
            #     pass
            #     # Display pick player modal
            # elif self._game_state.get_state() == GameStatus.MOVE_PIECE:
            #     # Draw all board locations
            #
            #     pass
            #     # Display board
            # elif self._game_state.get_state() == GameStatus.MAKE_SUGG:
            #     make_sugg.draw(gameDisplay, pygame.mouse)
            #
            #     # Display Suggestion Dialog
            # elif self._game_state.get_state() == GameStatus.ANSWER_SUGG:
            #     answer_sugg.draw(gameDisplay, pygame.mouse)
            #
            #     # Display Answer Suggestion Dialog
            # elif self._game_state.get_state() == GameStatus.MAKE_ACCUS:
            #     make_acc.draw(gameDisplay, pygame.mouse)

                # Display make accusation dialog


            pygame.display.update()

            clock.tick(60)


    def disconnect(self):
        return True

GameApp(None, GameState(), None, None)
