from SpyceInvaders import settings
from SpyceInvaders.actor import Actor


class Entity(Actor):

    def __init__(self, name, x, y, speed=0, cooldown=0):
        super().__init__(name, x, y)
        self.speed = speed
        self.cooldown = cooldown

    def move(self, direction, steps=1):
        if direction == settings.LEFT and self.rectangle.x > 0:
            self.rectangle.x = self.rectangle.x - self.speed * steps
        elif direction == settings.RIGHT and self.rectangle.x < settings.SCREEN_WIDTH - self.rectangle.width:
            self.rectangle.x = self.rectangle.x + self.speed * steps
        elif direction == settings.DOWN and self.rectangle.y < settings.SCREEN_HEIGHT - self.rectangle.height:
            self.rectangle.y = self.rectangle.y + self.speed * steps
        elif direction == settings.UP and self.rectangle.y > 0:
            self.rectangle.y = self.rectangle.y - self.speed * steps
        else:
            return True

