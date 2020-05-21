"""Defines building based on actor."""

from spyce_invaders import settings
from spyce_invaders.actor import Actor


class Building(Actor):
    """Creates destructible building."""

    def __init__(self, x, y, filename="building.png"):
        super().__init__(filename, x, y)
        self.destructible = True
        self.health_points = settings.BUILDING_HP
        self.score = settings.BUILDING_SCORE

    def receive_damage(self):
        """Subtract building health points and increase transparency.
        Overrides method from Actor."""
        if self.destructible and self.health_points is not None:
            self.health_points = self.health_points - settings.BULLET_DAMAGE
            self.image.set_alpha(255 * (self.health_points / settings.BUILDING_HP))
