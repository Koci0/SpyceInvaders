import pygame


class Entity(object):

    def __init__(self, name, x=0, y=0):
        self.image = pygame.image.load("data/" + str(name) + ".png").convert_alpha()
        self.rectangle = self.image
        self.x = x
        self.y = y
