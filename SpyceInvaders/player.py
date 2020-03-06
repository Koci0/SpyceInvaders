from SpyceInvaders.creature import Creature


class Player(Creature, object):

    def __init__(self, x, y, name="player"):
        super().__init__(name, x, y)
        self.speed = 5
