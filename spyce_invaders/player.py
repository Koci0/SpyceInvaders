"""Defines Player class based on Entity."""

import pygame.time

from spyce_invaders import settings
from spyce_invaders.bullet import Bullet
from spyce_invaders.entity import Entity


class Player(Entity):
    """Creates destructible entity with ability to move and shoot."""

    def __init__(self, x, y, filename="player.png"):
        super().__init__(filename, x, y)
        self.destructible = True
        self.health_points = settings.PLAYER_HP
        self.speed = 5
        self.cooldown = 100
        self.last_shot = pygame.time.get_ticks()

    def shoot(self, direction=settings.UP):
        """If cooldown allows it, shoots new bullet from current position."""
        now = pygame.time.get_ticks()
        if now - self.last_shot >= self.cooldown:
            self.last_shot = now
            return self.spawn_bullet(direction)
        return None

    def spawn_bullet(self, direction):
        """Creates bullet object in player's coordinates and returns it."""
        bullet = Bullet(self.rectangle.x + 0.5 * self.rectangle.width, self.rectangle.y, direction)
        return bullet
