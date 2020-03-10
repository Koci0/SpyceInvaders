import SpyceInvaders.settings as settings
from SpyceInvaders.entity import Entity


class Creature(Entity, object):

    def __init__(self, name, x, y, speed=0):
        super().__init__(name, x, y)
        self.speed = speed

    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x = self.x - self.speed
        if direction == "right" and self.x <= settings.screen_width - self.rectangle.width:
            self.x = self.x + self.speed
