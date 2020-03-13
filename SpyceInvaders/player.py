from SpyceInvaders.entity import Entity


class Player(Entity, object):

    def __init__(self, x, y, name="player"):
        super().__init__(name, x, y)
        self.speed = 5
