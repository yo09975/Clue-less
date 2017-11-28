"""user_interface.py"""
import pygame

pygame.init()

# Setting the display frame and title
gameDisplay = pygame.display.set_mode((1410, 900))
pygame.display.set_caption('Clue-less')
background = pygame.image.load('../data/clue-less_board.png')
clock = pygame.time.Clock()

# setting dummy conditions for displaying board - TEMPORARY
crashed = False

while not crashed:

    gameDisplay.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        print(event)

    pygame.display.update()

    clock.tick(60)


class UserInterface(object):
    """
    Defines interface between networking subsystem and the UI.  Game State will
    provide necessary information to be displayed on the UI (Game State, Game Board)
    """

    game_state = None   # reference to the GameState representing the current game
    board = None    # reference to the game board

    def __init__(self, game_state, board):
        self.__game_state = game_state
        self.__board = board

    def update():
        return True
