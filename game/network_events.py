from pygame import Vector2 as vec2
from game.snake import Snake


class ConnectionAcceptEvent:
    def __init__(self):
        pass


class RegisterWithServerEvent:
    def __init__(self):
        pass


class AssignIDEvent:
    def __init__(self, uid: str):
        self.id = uid


class AddSnakeEvent:
    def __init__(self, uid: str, snake: Snake):
        self.id = uid
        self.snake = snake


class SnakeUpdateEvent:
    def __init__(self, uid: str, snake: Snake):
        self.id = uid
        self.snake = snake


class FoodSpawnEvent:
    def __init__(self, position: vec2, color: tuple[int, int, int], mass: int):
        self.pos = position
        self.color = color
        self.mass = mass
