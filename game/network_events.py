from pygame import Vector2 as vec2
from snake import Snake


class SnakeUpdateEvent:
    def __init__(self, uid: str, snake: Snake):
        self.id = uid
        self.snake = snake


class FoodSpawnEvent:
    def __init__(self, position: vec2, color: tuple[int, int, int], mass: int):
        self.pos = position
        self.color = color
        self.mass = mass
