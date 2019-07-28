import pygame

# width and height of pygame window are set to 500, 500 
width, height = 1200, 700
title = "Python.io"
# background is set to black by default, pygame interprets color in RGB (red, green, blue) values
background = (0, 0, 0)

clock = pygame.time.Clock()
running = True

# initializing main pygame window
win = pygame.display.set_mode((width, height))
pygame.display.set_caption(title)
