import sys, os
import pygame

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from src.view import View

pygame.init()
gameDisplay = pygame.display.set_mode((800, 600))
crashed = False

clock = pygame.time.Clock()

top_view = View(0, 0, 200, 400)
top_view.fill(pygame.Color(100, 0, 0))
top_view.set_alpha(255)

sub_view = View(10, 10, 180, 380)
sub_view.fill(pygame.Color(0, 100, 0))
sub_view.set_alpha(255)

# Add sub_view as a subview to top_view
top_view.add_view(sub_view)

sub_sub_view = View(20, 20, 100, 300)
sub_sub_view.fill(pygame.Color(0, 0, 100))
sub_sub_view.set_alpha(255)

# Add sub_sub_view as a subview to sub_sub_view
sub_view.add_view(sub_sub_view)

overlapping_view = View(50, 50, 300, 50)
overlapping_view.fill(pygame.Color(100, 100, 0))
overlapping_view.set_alpha(255)


# ENTER MAIN GAME LOOP
while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    # To draw, call view.draw() and pass the mouse input and gameDisplay
    # Drawing a view will draw all subviews
    top_view.draw(pygame.mouse, gameDisplay)

    # Drawing is executed in order, last drawn will be on top
    overlapping_view.draw(pygame.mouse, gameDisplay)

    pygame.display.update()

    clock.tick(120)
