from SpyceInvaders import settings
from SpyceInvaders.actor import Actor


class Building(Actor):

    def __init__(self, x, y, filename="building.png"):
        super().__init__(filename, x, y)
        self.destructible = True
        self.hp = settings.BUILDING_HP

    def receive_damage(self):
        if self.destructible and self.hp is not None:
            self.hp = self.hp - settings.BULLET_DAMAGE
            self.image.set_alpha(255 * (self.hp / settings.BUILDING_HP))
