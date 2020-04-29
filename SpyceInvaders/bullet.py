from SpyceInvaders import settings
from SpyceInvaders.entity import Entity


class Bullet(Entity):

    def __init__(self, x, y, direction, bullet_type, filename="bullet.png"):
        super().__init__(filename, x, y)
        self.speed = settings.BULLET_SPEED
        self.direction = direction
        self.type = bullet_type

    def tick(self):
        return self.move(self.direction)
