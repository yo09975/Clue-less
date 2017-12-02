"""game_app.py"""
#import user_interface
import pygame
import sys
sys.path.append("..")
from src.gamestate import GameState
from src.notecard_controller import NoteCardController
from src.notecard import NoteCard
from src.user_interface import UserInterface
from src.gamestatus import GameStatus
from src.button import Button

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
        self._game_state = game_state

        self.__note_card = note_card
        self.__note_card_controller = note_card_controller

        pygame.init()
        gameDisplay = pygame.display.set_mode((800, 600))
        crashed = False

        game_img = pygame.image.load('../resources/gameplaygui.jpg')
        pick_players = Button((100,200))
        r = (10,10)
        pick_players.set_xy(r)
        make_suggestion = Button((100,200))

        # Always display the board and notecard
        # ENTER MAIN GAME LOOP
        while not crashed:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True

            gameDisplay.blit(game_img, (0, 0))

            # Detect state and draw accordingly
            if self._game_state.get_state() == GameStatus.LOBBY:
                pick_players.draw(gameDisplay, pygame.mouse)

                pass
                # Display pick player modal
            elif self._game_state.get_state() == GameStatus.MOVE_PIECE:
                pass
                # Display board
            elif self._game_state.get_state() == GameStatus.MAKE_SUGG:
                gameDisplay.blit(make_suggestion, (200,200))
                pass
                # Display Suggestion Dialog
            elif self._game_state.get_state() == GameStatus.ANSWER_SUGG:
                pass
                # Display Answer Suggestion Dialog
            elif self._game_state.get_state() == GameStatus.MAKE_ACCUS:
                pass
                # Display make accusation dialog


            pygame.display.update()

            clock.tick(120)


    def disconnect(self):
        return True

GameApp(None, GameState(), None, None)
