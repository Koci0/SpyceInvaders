"""Defines base class for every actor in game"""

import os.path

import pygame.image

from spyce_invaders import settings


class Actor:
    """Loads actor with image, rectangle, destructibility and health points in given x,y."""

    def __init__(self, filename, x, y):
        self.image = pygame.image.load(os.path.join(settings.DATA_PATH, filename)).convert_alpha()
        self.rectangle = self.image.get_rect()
        self.rectangle.x = x
        self.rectangle.y = y
        self.destructible = False
        self.health_points = None

    def is_alive(self):
        """Checks if health points are lower than or equal to 0."""
        if self.health_points is not None and self.health_points <= 0:
            return False
        return True

    def is_collided_with(self, actor):
        """Checks if rectangle is collided with another actor's rectangle."""
        return self.rectangle.colliderect(actor.rectangle)

    def receive_damage(self):
        """Subtracts actor health points if is destructible."""
        if self.destructible and self.health_points is not None:
            self.health_points -= settings.BULLET_DAMAGE
