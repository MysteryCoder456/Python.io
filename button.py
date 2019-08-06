import pygame
pygame.font.init()


class Button:
    def __init__(self, window, x, y, width, height, text='', text_size=10):
        self.window = window
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_size = text_size
        self.color = (255, 255, 255)
        self.text_color = (0, 0, 0)
        self.rect = (self.x, self.y, self.width, self.height)
        self.font = pygame.font.SysFont('Comic Sans MS', self.text_size)

    def clicked(self):
        mouse = pygame.mouse.get_pos()
        mouse_x = mouse[0]
        mouse_y = mouse[1]
        mouse_press = pygame.mouse.get_pressed()

        if mouse_press[0]:
            if mouse_x > self.x and mouse_x < self.x + self.width:
                if mouse_y > self.y and mouse_y < self.y + self.height:
                    return True

    def draw(self):
        pygame.draw.rect(self.window, self.color, self.rect)
        text = self.font.render(self.text, True, self.text_color)
        x = self.x + 20
        y = self.y + 10
        self.window.blit(text, (x, y))
