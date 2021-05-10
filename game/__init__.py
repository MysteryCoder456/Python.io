import pygame
from pygame import Vector2 as vec2


class PythonIO:
    def __init__(self):
        self.window_size = vec2(1024, 720)
        self.window = pygame.display.set_mode((int(self.window_size.x), int(self.window_size.y)), vsync=1)
        pygame.display.set_caption("Python.io Remastered")

        self.clock = pygame.time.Clock()
        self.running = True
        self.bg_color = (0, 0, 0)

    def update(self, delta_time: float):
        pygame.display.set_caption(f"Python.io Remastered - {int(self.clock.get_fps())} FPS")

        self.window.fill(self.bg_color)

        rect = pygame.Surface(vec2(50, 50))
        rect.fill((255, 0, 0))
        self.window.blit(rect, (100, 100))

        pygame.display.flip()
