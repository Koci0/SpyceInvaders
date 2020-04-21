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
        self.font_small = pygame.font.SysFont("mono", 16)
        self.font_big = pygame.font.SysFont("mono", 32)

    def update_surface(self):
        pygame.display.flip()
        self.surface.blit(self.background, (0, 0))

    def draw_text(self, text, x=0, y=0):
        surface = self.font_small.render(text, True, settings.white)
        self.surface.blit(surface, (x, y))

    def draw_center_text(self, text):
        lines = text.split("\n")
        for i in range(len(lines)):
            surface = self.font_big.render(lines[i], True, settings.white)
            line_width, line_height = self.font_big.size(lines[i])
            self.surface.blit(surface, (
                (settings.screen_width - line_width) // 2,
                (settings.screen_height // 2) + (1.5 * line_height * (i - (len(lines) // 2)))
            ))

    def draw_health_bar(self, percent):
        width = settings.health_bar_width
        height = settings.health_bar_height
        border = settings.health_bar_border
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

    def draw_building(self, building):
        width = building.rectangle.width
        height = building.rectangle.height
        surface = pygame.Surface((width, height))
        for h in range(height):
            for w in range(width):
                if building.grid[h][w] == 1:
                    rect = pygame.Rect(w, h, 1, 1)
                    pygame.draw.rect(surface, settings.blue, rect)

        self.surface.blit(surface, (building.rectangle.x, building.rectangle.y))
