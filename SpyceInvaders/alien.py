from SpyceInvaders import settings
from SpyceInvaders.bullet import Bullet
from SpyceInvaders.entity import Entity


class Alien(Entity):

    def __init__(self, x, y, direction="left", filename="alien.png"):
        super().__init__(filename, x, y)
        self.destructible = True
        self.hp = settings.ALIEN_HP
        self.speed = 1.0
        self.direction = direction
        self.score = settings.ALIEN_SCORE

    def tick(self):
        if self.move(self.direction):
            return True
        return False

    def swap_direction(self):
        if self.direction == settings.LEFT:
            self.direction = settings.RIGHT
        else:
            self.direction = settings.LEFT

    def spawn_bullet(self, direction, bullet_type):
        bullet = Bullet(self.rectangle.x + 0.5 * self.rectangle.width, self.rectangle.y, direction, bullet_type)
        return bullet
