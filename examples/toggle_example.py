import sys, os
import pygame

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from src.view import View
from src.toggle import Toggle

pygame.init()
gameDisplay = pygame.display.set_mode((800, 600))
crashed = False

clock = pygame.time.Clock()

toggle1 = Toggle(20, 20, 100, 100)
toggle1.set_alpha(255)
toggle2 = Toggle(140, 20, 100, 100)
toggle2.set_alpha(255)

def toggle_default(args):
    if args['b'].get_selected():
        args['b'].fill(pygame.Color(0, 255, 0))
    else:
        args['b'].fill(pygame.Color(255, 0, 0))


toggle1.set_default_action(toggle_default, {'b': toggle1})
toggle1.set_enabled(True)
toggle2.set_default_action(toggle_default, {'b': toggle2})

backgroundview = View(0, 0, 800, 600)
backgroundview.fill(pygame.Color(255, 255, 255))


# ENTER MAIN GAME LOOP
while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    backgroundview.draw(pygame.mouse, gameDisplay)

    toggle1.draw(pygame.mouse, gameDisplay)
    toggle2.draw(pygame.mouse, gameDisplay)


    pygame.display.update()

    clock.tick(60)
