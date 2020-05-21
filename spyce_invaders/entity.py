"""Defines base class for all actors with the ability to move based on Actor."""

from spyce_invaders import settings
from spyce_invaders.actor import Actor


class Entity(Actor):
    """Creates entity with speed and cooldown attributes."""

    def __init__(self, name, x, y, speed=0, cooldown=0):
        super().__init__(name, x, y)
        self.speed = speed
        self.cooldown = cooldown

    def move(self, direction, steps=1):
        """Moves entity in given direction by given steps, after checking coordinate boundaries.
        Returns False on failure, True otherwise."""
        if direction == settings.LEFT and self.rectangle.x > 0:
            self.rectangle.x -= self.speed * steps
            return True
        if direction == settings.RIGHT and \
                self.rectangle.x < settings.SCREEN_WIDTH - self.rectangle.width:
            self.rectangle.x += self.speed * steps
            return True
        if direction == settings.DOWN and \
                self.rectangle.y < settings.SCREEN_HEIGHT - self.rectangle.height:
            self.rectangle.y += self.speed * steps
            return True
        if direction == settings.UP and self.rectangle.y > 0:
            self.rectangle.y -= self.speed * steps
            return True
        return False
