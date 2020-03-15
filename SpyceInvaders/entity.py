import SpyceInvaders.settings as settings

from SpyceInvaders.actor import Actor


class Entity(Actor, object):

    def __init__(self, name, x, y, speed=0, cooldown=0):
        super().__init__(name, x, y)
        self.speed = speed
        self.cooldown = cooldown

    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x = self.x - self.speed
        elif direction == "right" and self.x < settings.screen_width - self.rectangle.width:
            self.x = self.x + self.speed
        elif direction == "down" and self.y < settings.screen_height - self.rectangle.height:
            self.y = self.y + self.speed
        elif direction == "up" and self.y > 0:
            self.y = self.y - self.speed
        else:
            return True
