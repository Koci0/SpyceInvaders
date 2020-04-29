import random

import pygame.time

from SpyceInvaders import settings
from SpyceInvaders.alien import Alien


class AlienGroup:

    def __init__(self, direction=settings.LEFT, rows=settings.ALIEN_GROUP_ROWS, columns=settings.ALIEN_GROUP_COLUMNS):
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
        for alien in self.aliens:
            alien.swap_direction()

    def shoot(self, direction=settings.DOWN, bullet_type="explosive"):
        now = pygame.time.get_ticks()
        if now - self.last_shot >= self.cooldown:
            self.last_shot = now
            if len(self.aliens) > 0:
                shooter = self.aliens[random.randint(0, len(self.aliens) - 1)]
                return shooter.spawn_bullet(direction, bullet_type)

    def remove(self, alien):
        self.aliens.remove(alien)
        self.increase_difficulty()

    def increase_difficulty(self):
        for alien in self.aliens:
            alien.speed += settings.DIFFICULTY_SPEED
        self.cooldown -= settings.DIFFICULTY_COOLDOWN
