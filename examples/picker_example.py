import sys, os
import pygame

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from src.view import View
from src.picker import Picker
from src.card import Card
from src.cardtype import CardType
from src.button import Button

pygame.init()
gameDisplay = pygame.display.set_mode((800, 600))
crashed = False

clock = pygame.time.Clock()

test_card1 = Card('Test Card 1 Name', CardType.SUSPECT, 'TEST111ID')
test_card2 = Card('Test Card 2 Name', CardType.SUSPECT, 'TEST222ID')
test_card3 = Card('Test Card 3 Name', CardType.SUSPECT, 'TEST333ID')
test_card4 = Card('Test Card 4 Name', CardType.SUSPECT, 'TEST444ID')
cards = [test_card1, test_card2, test_card3, test_card4]

picker1 = Picker(cards, 0, 0, 200, 200)
picker1.fill(pygame.Color(0, 0, 255))

picker2 = Picker(cards, 300, 0, 200, 200)
picker2.fill(pygame.Color(0, 0, 255))
picker2.disable_button(3)

def button_action(args):
    picker = args['p']
    if (picker.get_selected()):
        print(picker.get_selected())

# Prints the selected card for picker1
button1 = Button(0, 220, 200, 40)
button1.set_on_click(button_action, {'p': picker1})

# Prints the selected card for picker2
button2 = Button(300, 220, 200, 40)
button2.set_on_click(button_action, {'p': picker2})

backgroundview = View(0, 0, 800, 600)
backgroundview.fill(pygame.Color(255, 255, 255))


# ENTER MAIN GAME LOOP
while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    backgroundview.draw(pygame.mouse, gameDisplay)

    picker1.draw(pygame.mouse, gameDisplay)

    picker2.draw(pygame.mouse, gameDisplay)

    button1.draw(pygame.mouse, gameDisplay)
    button2.draw(pygame.mouse, gameDisplay)


    pygame.display.update()

    clock.tick(60)
