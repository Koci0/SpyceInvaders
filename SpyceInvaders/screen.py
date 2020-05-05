import pygame.display
import pygame.surface

from SpyceInvaders import settings


class Screen:

    def __init__(self, width=settings.SCREEN_WIDTH, height=settings.SCREEN_HEIGHT):
        pygame.display.set_caption("Press ESC to quit")
        self.width = width
        self.height = height
        self.surface = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface(self.surface.get_size()).convert()
        self.background.fill(settings.BACKGROUND_COLOR)
        self.font_small = pygame.font.SysFont("mono", 16)
        self.font_big = pygame.font.SysFont("mono", 32)

    def update_surface(self):
        pygame.display.flip()
        self.surface.blit(self.background, (0, 0))

    def draw_text(self, text, x=0, y=0):
        surface = self.font_small.render(text, True, settings.TEXT_COLOR)
        self.surface.blit(surface, (x, y))

    def draw_center_text(self, text):
        lines = text.split("\n")
        for i in range(len(lines)):
            surface = self.font_big.render(lines[i], True, settings.TEXT_COLOR)
            line_width, line_height = self.font_big.size(lines[i])
            self.surface.blit(surface, (
                (settings.SCREEN_WIDTH - line_width) // 2,
                (settings.SCREEN_HEIGHT // 2) + (1.5 * line_height * (i - (len(lines) // 2)))
            ))

    def draw_health_bar(self, percent):
        width = settings.HEALTH_BAR_WIDTH
        height = settings.HEALTH_BAR_HEIGHT
        border = settings.HEALTH_BAR_BORDER
        surface = pygame.Surface((2 * width + 2 * border, height + 2 * border))
        # Border rectangle
        rect = pygame.Rect(0, 0, width + 2 * border, height + 2 * border)
        pygame.draw.rect(surface, settings.HEALTH_BAR_COLOR, rect)
        # Current hp rectangle
        if percent < 100:
            rect = pygame.Rect(border + width, border, -(width - percent), height)
            pygame.draw.rect(surface, settings.BACKGROUND_COLOR, rect)

        self.surface.blit(surface, (0, 20))

    def draw_entity(self, entity):
        self.surface.blit(entity.image, (entity.rectangle.x, entity.rectangle.y))
