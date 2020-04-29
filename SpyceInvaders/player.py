import pygame.time

from SpyceInvaders import settings
from SpyceInvaders.bullet import Bullet
from SpyceInvaders.entity import Entity


class Player(Entity):

    def __init__(self, x, y, filename="player.png"):
        super().__init__(filename, x, y)
        self.destructible = True
        self.hp = settings.PLAYER_HP
        self.speed = 5
        self.cooldown = 100
        self.last_shot = pygame.time.get_ticks()

    def shoot(self, direction=settings.UP):
        now = pygame.time.get_ticks()
        if now - self.last_shot >= self.cooldown:
            self.last_shot = now
            return self.spawn_bullet(direction)
        return None

    def spawn_bullet(self, direction):
        bullet = Bullet(self.rectangle.x + 0.5 * self.rectangle.width, self.rectangle.y, direction, "normal")
        return bullet
