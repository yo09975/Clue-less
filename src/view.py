"""view.py"""
import pygame
from button import Button

pygame.init()

# Setting the display frame and title
pygame.display.set_caption('Clue-less')
game_display = pygame.display.set_mode((1410, 900), pygame.FULLSCREEN)
background = pygame.image.load('../data/clue-less_board.png')
clock = pygame.time.Clock()

green = (0, 200, 0)

class View:
    def draw_board(self):
        # setting conditions for displaying board
        crashed = False

        while not crashed:

            game_display.blit(background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True

                print(event)

            x = 50
            y = 50

            # render room buttons
            for i in range(3):
                room_btn = Button(game_display, x, y)
                for j in range (3):
                    room_btn = Button(game_display, x, y)
                    y = y + 100
                y = 50
                x = x + 200

            pygame.display.update()

            clock.tick(60)

new_view = View()
new_view.draw_board()
