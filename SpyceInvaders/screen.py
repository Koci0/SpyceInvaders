import pygame

black = (0, 0, 0)
white = (255, 255, 255)


class Screen(object):

    def __init__(self, width=800, height=400):
        pygame.init()
        pygame.display.set_caption("Press ESC to quit")
        self.width = width
        self.height = height
        self.surface = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface(self.surface.get_size()).convert()
        self.background.fill(black)
        self.font = pygame.font.SysFont("mono", 16)

    def draw_text(self, text):
        fw, fh = self.font.size(text)
        surface = self.font.render(text, True, white)
        self.surface.blit(surface, (0, 0))

    def draw_entity(self, entity):
        self.surface.blit(entity.image, (entity.x, entity.y))
