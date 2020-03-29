import pygame

import SpyceInvaders.settings as settings


class Screen(object):

    def __init__(self, width=settings.screen_width, height=settings.screen_height):
        pygame.init()
        pygame.display.set_caption("Press ESC to quit")
        self.width = width
        self.height = height
        self.surface = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface(self.surface.get_size()).convert()
        self.background.fill(settings.black)
        self.font = pygame.font.SysFont("mono", 16)

    def draw_text(self, text):
        fw, fh = self.font.size(text)
        surface = self.font.render(text, True, settings.white)
        self.surface.blit(surface, (0, 0))

    def draw_health_bar(self, percent):
        width = 100
        height = 12
        border = 4
        surface = pygame.Surface((2 * width + 2 * border, height + 2 * border))
        # Border rectangle
        rect = pygame.Rect(0, 0, width + 2 * border, height + 2 * border)
        pygame.draw.rect(surface, settings.red, rect)
        # Current hp rectangle
        if percent < 100:
            rect = pygame.Rect(border + width, border, -(width - percent), height)
            pygame.draw.rect(surface, settings.black, rect)

        self.surface.blit(surface, (0, 20))

    def draw_entity(self, entity):
        self.surface.blit(entity.image, (entity.rectangle.x, entity.rectangle.y))
