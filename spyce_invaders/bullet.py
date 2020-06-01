"""Defines Bullet class based on Entity."""

from spyce_invaders import settings
from spyce_invaders.entity import Entity


class Bullet(Entity):
    """Creates indestructible entity."""

    def __init__(self, x, y, direction, filename="bullet.png"):
        super().__init__(filename, x, y)
        self.speed = settings.BULLET_SPEED
        self.direction = direction

    def tick(self):
        """Moves bullet and returns if the method was successful."""
        return not self.move(self.direction)
