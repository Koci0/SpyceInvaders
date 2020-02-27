import pygame
import sys


def run():
    pygame.init()

    size = (width, height) = 800, 600
    black = (0, 0, 0)

    screen = pygame.display.set_mode(size)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(black)
        pygame.display.flip()
