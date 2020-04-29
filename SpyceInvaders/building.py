from SpyceInvaders import settings
from SpyceInvaders.actor import Actor


class Building(Actor):

    def __init__(self, x, y, filename="building.png"):
        super().__init__(filename, x, y)
        self.destructible = True
        self.hp = self.rectangle.width * self.rectangle.height
        self.grid = [[1 for _ in range(self.rectangle.width)] for _ in range(self.rectangle.height)]

    def receive_damage(self, bullet):
        x = bullet.rectangle.x - self.rectangle.x
        hit_point_x = x
        hit_point_y = 0
        if bullet.direction == settings.DOWN:
            for y in range(self.rectangle.height):
                if self.grid[y][x] == 1:
                    hit_point_y = y
                    break
        elif bullet.direction == settings.UP:
            for y in range(self.rectangle.height - 1, -1, -1):
                if self.grid[y][x] == 1:
                    hit_point_y = y
                    break

        if bullet.type == "normal":
            for dx in range(bullet.rectangle.width):
                if 0 <= hit_point_x + dx < self.rectangle.width:
                    self.grid[hit_point_y][hit_point_x + dx] = 0
        elif bullet.type == "explosive":
            for dy in range(settings.EXPLOSION_RADIUS + 1):
                for dx in range(-settings.EXPLOSION_RADIUS, settings.EXPLOSION_RADIUS + 1):
                    y_coord = hit_point_y + dy
                    x_coord = hit_point_x + dx
                    if 0 <= x_coord < self.rectangle.width:
                        self.grid[y_coord][x_coord] = 0
