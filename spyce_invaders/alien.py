"""Defines Alien class based on Entity."""

from spyce_invaders import settings
from spyce_invaders.bullet import Bullet
from spyce_invaders.entity import Entity


class Alien(Entity):
    """Creates destructible entity with constant movement direction."""

    def __init__(self, x, y, direction="left", filename="alien.png"):
        super().__init__(filename, x, y)
        self.destructible = True
        self.health_points = settings.ALIEN_HP
        self.speed = 1.0
        self.direction = direction
        self.score = settings.ALIEN_SCORE

    def tick(self):
        """Tries to move alien, returns True on success and False of failure."""
        if not self.move(self.direction):
            return True
        return False

    def swap_direction(self):
        """Swaps alien's direction (horizontally)."""
        if self.direction == settings.LEFT:
            self.direction = settings.RIGHT
        else:
            self.direction = settings.LEFT

    def spawn_bullet(self, direction):
        """Creates bullet object in alien's coordinates and returns it."""
        bullet = Bullet(self.rectangle.x + 0.5 * self.rectangle.width, self.rectangle.y, direction)
        return bullet
