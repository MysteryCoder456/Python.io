from uni_vars import *
from sprite import Sprite
import pygame


class Food(Sprite):
	def __init__(self, x, y, color):
		super().__init__(x, y, 5)
		self.color = color

	def render(self):
		pygame.draw.ellipse(win, self.color, (self.draw_x, self.draw_y, self.size * 2, self.size * 2))
