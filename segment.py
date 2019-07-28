from uni_vars import *
from sprite import Sprite
import pygame


class Segment(Sprite):
    def __init__(self, x, y, size, color):
        super().__init__(x, y, size)
        self.color = color
        # self.outline_size = 3
        # self.outline_color = (0, 200, 0)

    def render(self):
        # pygame.draw.ellipse(win, self.outline_color, (self.draw_x, self.draw_y, self.size * 2 + self.outline_size, self.size * 2 + self.outline_size))
        pygame.draw.ellipse(win, self.color, (self.draw_x, self.draw_y, self.size * 2, self.size * 2))