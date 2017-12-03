import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import pygame
from src.pybutton import PyButton

game_img = pygame.image.load('../data/clue-less_board.png')

pygame.init()
gameDisplay = pygame.display.set_mode((800, 600))
crashed = False

clock = pygame.time.Clock()

big_button = PyButton(10, 10, 200, 200)


def big_clicked(args):
    args['b'].fill(pygame.Color(100,0,0))

def big_hover(args):
    args['b'].fill(pygame.Color(0,0,100))

big_button.set_on_click(big_clicked, {'b': big_button})
big_button.set_on_hover_action(big_hover, {'b': big_button})

sm_button_1 = PyButton(20, 20, 50, 50)
sm_button_2 = PyButton(70, 70, 50, 50)

big_button.add_view(sm_button_1)
big_button.add_view(sm_button_2)


# Always display the board and notecard
# ENTER MAIN GAME LOOP
while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    gameDisplay.blit(game_img, (0, 0))

    big_button.draw(pygame.mouse, gameDisplay)

    pygame.display.update()

    clock.tick(120)
