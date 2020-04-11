import SpyceInvaders.settings as settings
from SpyceInvaders.entity import Entity


class Bullet(Entity, object):

    def __init__(self, x, y, direction, bullet_type, name="bullet"):
        super().__init__(name, x, y)
        self.speed = settings.bullet_speed
        self.direction = direction
        self.type = bullet_type

    def tick(self):
        return self.move(self.direction)
