from SpyceInvaders.entity import Entity


class Alien(Entity, object):

    def __init__(self, x, y, direction="left", name="alien"):
        super().__init__(name, x, y, speed=1)
        self.direction = direction

    def tick(self):
        if self.move(self.direction):
            return True
        return False

    def swap_direction(self):
        if self.direction == "left":
            self.direction = "right"
        else:
            self.direction = "left"
