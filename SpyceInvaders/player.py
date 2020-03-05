from SpyceInvaders.entity import Entity


class Player(Entity, object):

    def __init__(self, name="player", x=0, y=0):
        super().__init__(name, x, y)
        self.speed = 3
