from SpyceInvaders.entity import Entity


class Bullet(Entity, object):

    def __init__(self, x, y, direction, type, name="bullet"):
        super().__init__(name, x, y, speed=5)
        self.direction = direction
        self.type = type

    def tick(self):
        return self.move(self.direction)
