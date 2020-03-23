import pygame


class Actor(object):

    def __init__(self, name, x, y, destructible=False, hp=None):
        self.image = pygame.image.load("data/" + str(name) + ".png").convert_alpha()
        self.rectangle = self.image.get_rect()
        self.x = x
        self.y = y
        self.destructible = destructible
        self.hp = hp

    def receive_damage(self, damage):
        if self.destructible and self.hp is not None:
            self.hp = self.hp - damage

    def is_alive(self):
        if self.hp is not None and self.hp <= 0:
            return False
        return True

    def is_collided_with(self, actor):
        return self.rectangle.colliderect(actor.rectangle)
