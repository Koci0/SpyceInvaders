import SpyceInvaders.settings as settings
from SpyceInvaders.actor import Actor


class Building(Actor, object):

    def __init__(self, x, y, name="building"):
        super().__init__(name, x, y)
        self.destructible = True
        self.hp = settings.building_hp
