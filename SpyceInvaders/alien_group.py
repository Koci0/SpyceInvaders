from random import randint

from pygame.time import get_ticks

import SpyceInvaders.settings as settings
from SpyceInvaders.alien import Alien


class AlienGroup(object):

    def __init__(self, direction="left", rows=5, columns=11):
        spacing = 0.75 * settings.screen_width // (columns - 1)
        self.rows = rows
        self.columns = columns
        self.aliens = []
        for i in range(self.rows):
            for j in range(self.columns):
                self.aliens.append(
                    Alien((j + 1) * spacing, (i + 1) * spacing))
        self.cooldown = 500
        self.last_shot = get_ticks()
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

        return self.shoot()

    def swap_direction(self):
        for alien in self.aliens:
            alien.swap_direction()

    def shoot(self, direction="down", type="explosive"):
        now = get_ticks()
        if now - self.last_shot >= self.cooldown:
            self.last_shot = now
            if len(self.aliens) > 0:
                shooter = self.aliens[randint(0, len(self.aliens) - 1)]
                return shooter.spawn_bullet(direction, type)
        return None

    def remove(self, alien):
        self.aliens.remove(alien)
        self.increase_difficulty()

    def increase_difficulty(self):
        for alien in self.aliens:
            alien.speed += settings.difficulty_speed
        self.cooldown -= settings.difficulty_cooldown
