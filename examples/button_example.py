"""
button_example.py.

This is a pretty complex example that shows the different functionalities of
buttons. There are three buttons - one large button and two smaller buttons.

When you start, you see only two buttons.
    When you click the large button it changes colors
    When you click the smaller button, it changes colors and enables a second
        smaller button.
    When you click on the second smaller button, it changes the functionality of
        the large button so that it turns a random color each time it's clicked.
"""

import sys, os
import pygame
import random

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from src.button import Button
from src.view import View

pygame.init()
gameDisplay = pygame.display.set_mode((800, 600))
crashed = False

clock = pygame.time.Clock()

big_button = Button(10, 10, 200, 200)


# Define a function to be executed when big button is clicked
def big_clicked(args):
    args['b'].fill(pygame.Color(100, 0, 0))
    args['b'].set_alpha(100)

# Define a fucntion to be executed when big button is hovered over
def big_hover(args):
    args['b'].fill(pygame.Color(0, 0, 100))
    args['b'].set_alpha(255)

# Set a default action. Really only useful for making Button a default color
def big_default(args):
    args['b'].fill(pygame.Color(0, 255, 0))
    args['b'].set_alpha(100)

# Set action, and pass big_button as a parameter
big_button.set_on_click(big_clicked, {'b': big_button})
big_button.set_on_hover_action(big_hover, {'b': big_button})
big_button.set_default_action(big_default, {'b': big_button})

# Create one button as a sub view of Button
sm_button_1 = Button(20, 20, 50, 50)
sm_button_2 = Button(70, 70, 50, 50)

# A button's action doesn't have to reference itself or a sub/superview
# For example, when sm_button_1 is clicked, change enabled status of sm_button_2
def sm_button_1_click(args):
    # This references a reference of sm_button_1 in args
    args['b'].fill(pygame.Color(100, 100, 0))
    # This references a local variable in button_example.py
    sm_button_2.set_enabled(True)

def sm_button_default(args):
    args['b'].fill(pygame.Color(0, 255, 0))
    args['b'].set_alpha(255)

sm_button_1.set_on_click(sm_button_1_click, {'b': sm_button_1})
sm_button_1.set_default_action(sm_button_default, {'b': sm_button_1})

big_button.add_view(sm_button_1)


def sm_button_2_click(args):
    # You can even set other button's click action in a click action
    def new_big_button_click(args):
        args['b'].fill(pygame.Color(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)))
    args['b'].set_on_click(new_big_button_click, {'b': args['b']})
    # This overwrites big_button's action
    # Now big button becomes a random color whenever it's clicked

sm_button_2.set_on_click(sm_button_2_click, {'b': big_button})
sm_button_2.set_default_action(sm_button_default, {'b': sm_button_2})
sm_button_2.set_enabled(False)


backgroundview = View(0, 0, 800, 600)
backgroundview.fill(pygame.Color(255, 255, 255))

# Always display the board and notecard
# ENTER MAIN GAME LOOP
while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
    # Make a white background
    backgroundview.draw(pygame.mouse, gameDisplay)

    big_button.draw(pygame.mouse, gameDisplay)

    sm_button_2.draw(pygame.mouse, gameDisplay)

    pygame.display.update()

    clock.tick(60)
