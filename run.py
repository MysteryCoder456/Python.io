import pygame

from game import PythonIO


def main():
    g = PythonIO()

    while g.running:
        delta_time = g.clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                g.running = False
                pygame.quit()
                return

        g.update(delta_time)


if __name__ == '__main__':
    main()
