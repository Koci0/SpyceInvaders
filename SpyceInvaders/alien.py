import SpyceInvaders.settings as settings
from SpyceInvaders.bullet import Bullet
from SpyceInvaders.entity import Entity


class Alien(Entity, object):

    def __init__(self, x, y, direction="left", name="alien"):
        super().__init__(name, x, y)
        self.destructible = True
        self.hp = settings.alien_hp
        self.speed = 1.0
        self.direction = direction

    def tick(self):
        if self.move(self.direction):
            return True
        return False

    def swap_direction(self):
        if self.direction == "left":
            self.direction = "right"
        else:
            self.direction = "left"

    def spawn_bullet(self, direction, bullet_type):
        bullet = Bullet(self.rectangle.x + 0.5 * self.rectangle.width, self.rectangle.y, direction, bullet_type)
        return bullet
