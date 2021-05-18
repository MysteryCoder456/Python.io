import pygame
from random import randint
from pygame import Vector2 as vec2

from game.client import ClientInterface
from game.snake import Snake
from game.network_events import *


class PythonIO:
    def __init__(self):
        pygame.init()

        self.window_size = vec2(1536, 900)
        self.window = pygame.display.set_mode(
            (int(self.window_size.x), int(self.window_size.y))
        )
        pygame.display.set_caption("Python.io Remastered")

        self.clock = pygame.time.Clock()
        self.running = True
        self.bg_color = (0, 0, 0)

        self.client = ClientInterface("127.0.0.1", 6969)
        self.players: dict[str, Snake] = {}

        self.waiting_for_server = True

    def update(self, delta_time: float):
        if not self.client.queue_empty():
            msg = self.client.pop_first_msg()

            if isinstance(msg, ConnectionAcceptEvent):
                print("Server has acknowledged your existence.")
                new_position = vec2(
                    randint(0, int(self.window_size.x / 2)),
                    randint(0, int(self.window_size.y))
                )
                new_snake = Snake(
                    new_position,
                    (randint(0, 255), randint(0, 255), randint(0, 255))
                )
                msg_register = RegisterWithServerEvent(new_snake)
                self.client.send(msg_register)

            elif isinstance(msg, AssignIDEvent):
                self.client.id = msg.id

            elif isinstance(msg, AddSnakeEvent):
                self.players[msg.id] = msg.snake

                if msg.id == self.client.id:
                    self.waiting_for_server = False

        pygame.display.set_caption(
            f"Python.io Remastered - {int(self.clock.get_fps())} FPS"
        )

        if not self.waiting_for_server:
            # Controls
            keys = pygame.key.get_pressed()
            self.players[self.client.id].boosting = keys[pygame.K_w]
            self.players[self.client.id].heading += (
                (keys[pygame.K_d] - keys[pygame.K_a])
                * self.players[self.client.id].turn_speed
                * delta_time
            )

        for uid in self.players:
            self.players[uid].update(delta_time)

        self.window.fill(self.bg_color)

        for uid in self.players:
            self.players[uid].draw(self.window)

        pygame.display.flip()

        if not self.waiting_for_server:
            msg_update_snake = SnakeUpdateEvent(self.client.id, self.players[self.client.id])
            self.client.send(msg_update_snake)
