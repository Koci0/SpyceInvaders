import SpyceInvaders.settings as settings
from SpyceInvaders.actor import Actor


class Building(Actor, object):

    def __init__(self, x, y, name="building"):
        super().__init__(name, x, y)
        self.destructible = True
        self.hp = self.rectangle.width * self.rectangle.height
        self.grid = [[1 for _ in range(self.rectangle.width)] for _ in range(self.rectangle.height)]

    def receive_damage(self, _, x, direction_from):
        x = x - self.rectangle.x
        if direction_from == "down":
            for y in range(self.rectangle.height):
                if self.grid[y][x] == 1:
                    self.grid[y][x] = 0
                    break
        elif direction_from == "up":
            for y in range(self.rectangle.height - 1, -1, -1):
                if self.grid[y][x] == 1:
                    self.grid[y][x] = 0
                    break
