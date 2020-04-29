import os.path

import pygame.image

from SpyceInvaders import settings


class Actor:

    def __init__(self, filename, x, y, destructible=False, hp=None):
        self.image = pygame.image.load(os.path.join(settings.DATA_PATH, filename)).convert_alpha()
        self.rectangle = self.image.get_rect()
        self.rectangle.x = x
        self.rectangle.y = y
        self.destructible = destructible
        self.hp = hp

    def is_alive(self):
        if self.hp is not None and self.hp <= 0:
            return False
        return True

    def is_collided_with(self, actor):
        return self.rectangle.colliderect(actor.rectangle)
