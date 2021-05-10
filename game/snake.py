from typing import Union

import pygame
import pygame.gfxdraw
from pygame import Vector2 as vec2


class Snake:
    def __init__(self, position: vec2, color: tuple[int, int, int]):
        self.head_pos = position
        self.head_radius = 20
        self.heading: float = 0
        self.speed: float = 100
        self.boost_speed: float = 120
        self.turn_speed = 120
        self.velocity = vec2()

        segment_spacing = 5
        self.tail: list[vec2] = [vec2() for _ in range(100)]
        self.color = color
        self.boosting = False

    def update(self, delta_time):
        # Make each tail segment "follow" the one in front of it
        tail_length = len(self.tail)
        for i in range(1, tail_length):
            self.tail[tail_length - i].update(self.tail[tail_length - (i + 1)])
        self.tail[0].update(self.head_pos)

        self.velocity.from_polar((self.speed, self.heading))
        self.head_pos += self.velocity * delta_time

    def draw(self, window: pygame.Surface):
        pygame.gfxdraw.filled_circle(
            window,
            int(self.head_pos.x),
            int(self.head_pos.y),
            self.head_radius,
            self.color,
        )

        for (i, tail_segment) in enumerate(self.tail):
            alpha = 1 - i / len(self.tail)
            pygame.gfxdraw.filled_circle(
                window,
                int(tail_segment.x),
                int(tail_segment.y),
                int(self.head_radius * 0.85),
                (
                    self.color[0] * alpha,
                    self.color[1] * alpha,
                    self.color[2] * alpha,
                ),
            )
