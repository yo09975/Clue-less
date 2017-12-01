"""game_app.py"""
#import user_interface
import pygame
from src.gamestate import GameState
from src.note_card_controller import NoteCardController
from src.notecard import NoteCard
from src.user_interface import UserInterface


class GameApp(UserInterface):
    """
    Triggered by controllers to update after a move or suggestion has been asked.
    Can also show new views due to user action (asking for a suggestion).  Extends UserInterface.


    note_card_view = None   # two-dimensional array of button objects representing the note card information
    note_card = None    # a reference to the current note_card
    note_card_controller = None    # a reference to the NoteCardController to send clicks
    """

    def __init__(self, interface: UserInterface, game_state: GameState, note_card: NoteCard, note_card_controller: NoteCardController):
        self._game_state = game_state

        self.__note_card_view = note_card_view
        self.__note_card = note_card
        self.__note_card_controller = note_card_controller

        pygame.init()
        gameDisplay = pygame.display.set_mode((800, 600))
        crashed = False

        # ENTER MAIN GAME LOOP
        while not crashed:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True

            pygame.display.update()



    def disconnect(self):
        return True
