from pygame.time import get_ticks

from SpyceInvaders.bullet import Bullet
from SpyceInvaders.entity import Entity


class Player(Entity, object):

    def __init__(self, x, y, name="player"):
        super().__init__(name, x, y)
        self.destructible = True
        self.hp = 100
        self.speed = 5
        self.cooldown = 100
        self.last_shot = get_ticks()

    def shoot(self, direction="up"):
        now = get_ticks()
        if now - self.last_shot >= self.cooldown:
            self.last_shot = now
            return self.spawn_bullet(direction)
        return None

    def spawn_bullet(self, direction):
        bullet = Bullet(self.x + 0.5 * self.rectangle.width, self.y, direction)
        return bullet
