import sys, os
import pygame

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from src.view import View
from src.character_picker_dialog import CharacterPickerDialog as CPD
from src.button import Button
from enum import Enum
from src.card import Card
from src.cardtype import CardType


pygame.init()
gameDisplay = pygame.display.set_mode((1000, 600))
crashed = False

clock = pygame.time.Clock()

dialog = CPD(60, 60)
dialog.get_top_button().fill(pygame.Color(0, 255, 0))
# dialog.set_alpha(255)
dialog.set_is_visible(False)



# Create a button that pulls up the dialog
button = Button(100, 100, 200, 50)
button.fill(pygame.Color(100, 100, 0))
button.set_alpha(255)

def show_dialog(args):

    s = Card("Colonel Mustard", CardType.SUSPECT, "Colonel Mustard")
    args['d'].set_unavailable_players([s])
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
