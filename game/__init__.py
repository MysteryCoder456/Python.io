import pygame
from pygame import Vector2 as vec2

from game.snake import Snake


class PythonIO:
    def __init__(self):
        self.window_size = vec2(1536, 900)
        self.window = pygame.display.set_mode((int(self.window_size.x), int(self.window_size.y)))
        pygame.display.set_caption("Python.io Remastered")

        self.clock = pygame.time.Clock()
        self.running = True
        self.bg_color = (0, 0, 0)

        self.player = Snake(self.window_size / 2, "green")

    def update(self, delta_time: float):
        pygame.display.set_caption(f"Python.io Remastered - {int(self.clock.get_fps())} FPS")

        self.player.update(delta_time)

        self.window.fill(self.bg_color)

        self.player.draw(self.window)

        pygame.display.flip()
