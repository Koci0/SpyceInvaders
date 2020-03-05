import pygame


class Entity(object):
    directions = {None: 0, "left": -1, "right": 1}

    def __init__(self, name, x=0, y=0, speed=0):
        self.image = pygame.image.load("data/" + str(name) + ".png").convert_alpha()
        self.rectangle = self.image
        self.x = x
        self.y = y
        self.direction = self.directions[None]
        self.speed = speed

    def move(self, direction):
        self.x = self.x + self.directions[direction] * self.speed
