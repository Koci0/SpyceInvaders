"""Defines group that contains all aliens on game screen."""

import random

import pygame.time

from spyce_invaders import settings
from spyce_invaders.alien import Alien


class AlienGroup:
    """Creates grid of aliens with common shooting cooldown and movement direction."""

    def __init__(self,
                 direction=settings.LEFT,
                 rows=settings.ALIEN_GROUP_ROWS,
                 columns=settings.ALIEN_GROUP_COLUMNS):
        spacing = settings.ALIEN_GROUP_SPACING * settings.SCREEN_WIDTH // (columns - 1)
        self.rows = rows
        self.columns = columns
        self.aliens = []
        for i in range(self.rows):
            for j in range(self.columns):
                self.aliens.append(
                    Alien((j + 1) * spacing, (i + 1) * spacing))
        self.cooldown = settings.ALIEN_GROUP_COOLDOWN
        self.last_shot = pygame.time.get_ticks()
        self.direction = direction

    def tick(self):
        """Moves every alien in the list, if one hits the bounds, everyone swaps direction.
        Then tries to shoot."""
        swap = False
        i = 0
        for alien in self.aliens:
            i += 1
            if alien:
                if alien.tick():
                    swap = True

        if swap:
            self.swap_direction()
            for alien in self.aliens:
                alien.move(settings.DOWN, steps=3)

        return self.shoot()

    def swap_direction(self):
        """Swaps movement direction of every alien."""
        for alien in self.aliens:
            alien.swap_direction()

    def shoot(self, direction=settings.DOWN, bullet_type="explosive"):
        """If cooldown allows it, shoots new bullet from random alien in the grid."""
        now = pygame.time.get_ticks()
        if now - self.last_shot >= self.cooldown:
            self.last_shot = now
            if len(self.aliens) > 0:
                shooter = self.aliens[random.randint(0, len(self.aliens) - 1)]
                return shooter.spawn_bullet(direction, bullet_type)

    def remove(self, alien):
        """Removes alien from the list and increases game difficulty."""
        self.aliens.remove(alien)
        self.increase_difficulty()

    def increase_difficulty(self):
        """Increases movement speed and decreases shooting cooldown."""
        for alien in self.aliens:
            alien.speed += settings.DIFFICULTY_SPEED
        self.cooldown -= settings.DIFFICULTY_COOLDOWN
