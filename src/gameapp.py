import sys, os
import pygame

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from src.view import View
from src.suggestion_dialog import SuggestionDialog as SD
from src.answer_suggestion_dialog import AnswerSuggestionDialog as ASD
from src.notecard_view import NoteCardView
from src.button import Button
from enum import Enum


class GameApp:
    def __init__():

        pygame.init()
        gameDisplay = pygame.display.set_mode((1000, 600))
        crashed = False

        # Set up different views

        # Set up Suggestion Dialog
        self._sugg_dialog = SD(60, 60)
        self._sugg_dialog.set_is_visible(False)

        # Set up Suggestion Response Dialog
        self._ans_sugg_dialog = ASD(60, 60)
        self._sugg_dialog.set_is_visible(False)

        # Set up character picker dialog
        # TODO waiting for merge

        # Set up board
        self._board = View(0, 0, 500, 500)
        self._board.set_alpha(100)
        self._board.fill(pygame.Color(0, 0, 255))
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, '../data/locations.json')

        with open(filename) as data_file:
            locs = json.load(data_file)

        for l in locs['locations']:
            def location_hover(args):
                args.fill(pygame.Color(255, 0, 0))
                args.set_alpha(100)

            def location_default(args):
                args.set_alpha(0)

            location = Button(l['dims']['x'], l['dims']['y'], l['dims']['width'], l['dims']['height'])
            location.set_default_action(location_default, location)
            location.set_on_hover_action(location_hover, location)

            board[l['key']] = location
            disp_board[l['key']] = location
            if l['type'] == "room":
                board[l['name']] = location

        # Set up note card
        self._note_card = NoteCardView(1231, 121)

        # Set up gameplay button

        clock = pygame.time.Clock()




# Set up all views



# Create a button that pulls up the dialog
button = Button(100, 100, 200, 50)
button.fill(pygame.Color(100, 100, 0))
button.set_alpha(255)

def show_dialog(args):
    args['d'].set_is_visible(True)

button.set_on_click(show_dialog, {'d': dialog})

backgroundview = View(0, 0, 1000, 1000)
backgroundview.fill(pygame.Color(255, 255, 255))
backgroundview.set_alpha(255)



# ENTER MAIN GAME LOOP
while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    backgroundview.draw(pygame.mouse, gameDisplay)

    # When a view isn't available, it's best to never draw it at all

    button.draw(pygame.mouse, gameDisplay)

    # Draw the dialog over the button if visible
    dialog.draw(pygame.mouse, gameDisplay)


    pygame.display.update()

    clock.tick(60)
