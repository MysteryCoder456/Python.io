from typing import Union

import pygame
from pygame import Vector2 as vec2, Color


class Snake:
    def __init__(self, position: vec2, color: Union[Color, str, tuple[int, int, int]]):
        self.head_pos = position
        self.head_radius = 20
        self.heading: float = 0
        self.speed: float = 70
        self.boost_speed: float = 105
        self.velocity = vec2()

        self.color = color
        self.tail: list[vec2] = [vec2() for _ in range(5)]

    def update(self, delta_time):
        self.velocity.from_polar((self.speed, self.heading))
        self.head_pos += self.velocity * delta_time

    def draw(self, window: pygame.Surface):
        pygame.draw.circle(window, self.color, self.head_pos, self.head_radius)
