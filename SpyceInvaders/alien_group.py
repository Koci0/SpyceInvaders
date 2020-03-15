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
        self.direction = direction

    def tick(self):
        swap = False
        for alien in self.aliens:
            if alien:
                if alien.tick():
                    swap = True

        if swap:
            self.swap_direction()

    def swap_direction(self):
        for alien in self.aliens:
            alien.swap_direction()

