import pygame


class Entity(object):

    def __init__(self, name, x, y):
        self.image = pygame.image.load("data/" + str(name) + ".png").convert_alpha()
        self.rectangle = self.image.get_rect()
        self.x = x
        self.y = y
