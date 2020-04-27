import SpyceInvaders.settings as settings

from SpyceInvaders.actor import Actor


class Entity(Actor, object):

    def __init__(self, name, x, y, speed=0, cooldown=0):
        super().__init__(name, x, y)
        self.speed = speed
        self.cooldown = cooldown

    def move(self, direction, steps=1):
        if direction == "left" and self.rectangle.x > 0:
            self.rectangle.x = self.rectangle.x - self.speed * steps
        elif direction == "right" and self.rectangle.x < settings.screen_width - self.rectangle.width:
            self.rectangle.x = self.rectangle.x + self.speed * steps
        elif direction == "down" and self.rectangle.y < settings.screen_height - self.rectangle.height:
            self.rectangle.y = self.rectangle.y + self.speed * steps
        elif direction == "up" and self.rectangle.y > 0:
            self.rectangle.y = self.rectangle.y - self.speed * steps
        else:
            return True
        return False

    def receive_damage(self, _):
        if self.destructible and self.hp is not None:
            self.hp = self.hp - settings.bullet_damage
