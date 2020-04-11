import SpyceInvaders.settings as settings
from SpyceInvaders.actor import Actor


class Building(Actor, object):

    def __init__(self, x, y, name="building"):
        super().__init__(name, x, y)
        self.destructible = True
        self.hp = self.rectangle.width * self.rectangle.height
        self.grid = [[1 for _ in range(self.rectangle.width)] for _ in range(self.rectangle.height)]

    def receive_damage(self, bullet_type, x, direction_from):
        x = x - self.rectangle.x
        hit_point_x = x
        hit_point_y = 0
        if direction_from == "down":
            for y in range(self.rectangle.height):
                if self.grid[y][x] == 1:
                    hit_point_y = y
                    break
        elif direction_from == "up":
            for y in range(self.rectangle.height - 1, -1, -1):
                if self.grid[y][x] == 1:
                    hit_point_y = y
                    break

        if bullet_type == "normal":
            self.grid[hit_point_y][hit_point_x] = 0
        elif bullet_type == "explosive":
            for dy in range(settings.explosion_radius + 1):
                for dx in range(-settings.explosion_radius, settings.explosion_radius + 1):
                    y_coord = hit_point_y + dy
                    x_coord = hit_point_x + dx
                    if 0 <= x_coord < self.rectangle.width:
                        self.grid[y_coord][x_coord] = 0
