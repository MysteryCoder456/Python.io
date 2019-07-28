import math


class Sprite:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.x_vel = 0
        self.y_vel = 0
        self.draw_x = self.x - self.size
        self.draw_y = self.y - self.size
        self.speed = 0
        self.angle = 0

    def update(self):
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed

        self.x += self.x_vel
        self.y += self.y_vel

        self.draw_x = self.x - self.size
        self.draw_y = self.y - self.size