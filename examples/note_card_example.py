import sys, os
import pygame

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from src.view import View
from src.notecard_view import NoteCardView
from enum import Enum

class DialogVisible(Enum):
    VISIBLE = 1
    NOT_VISIBLE = 2


pygame.init()
gameDisplay = pygame.display.set_mode((1410, 900))
crashed = False

clock = pygame.time.Clock()

nc = NoteCardView(1231, 121)

backgroundview = View(0, 0, 1000, 1000)
backgroundview.fill(pygame.Color(255, 255, 255))
backgroundview.set_alpha(255)

background = pygame.image.load('resources/gameplaygui.jpg')


# ENTER MAIN GAME LOOP
while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    gameDisplay.blit(background, (0, 0))

    # When a view isn't available, it's best to never draw it at all

    nc.draw(pygame.mouse, gameDisplay)

    pygame.display.update()

    clock.tick(60)
