"""Defines class that handles drawing on the screen."""

import pygame.display
import pygame.surface

from spyce_invaders import settings


class Screen:
    """Creates canvas for drawing of entities. Has single surface and background to
    optimize rendering. Defines small and big font sizes."""

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
        """Draws current surface onto screen and cleans it for next frame with background."""
        pygame.display.flip()
        self.surface.blit(self.background, (0, 0))

    def draw_text(self, text, x_coordinate=0, y_coordinate=0):
        """Draws given string on the surface at given coordinates with small font."""
        surface = self.font_small.render(text, True, settings.TEXT_COLOR)
        self.surface.blit(surface, (x_coordinate, y_coordinate))

    def draw_center_text(self, text):
        """Draws given test on the surface centered horizontally and vertically with big font."""
        lines = text.split("\n")
        for i, line in enumerate(lines):
            surface = self.font_big.render(line, True, settings.TEXT_COLOR)
            line_width, line_height = self.font_big.size(line)
            self.surface.blit(surface, (
                (settings.SCREEN_WIDTH - line_width) // 2,
                (settings.SCREEN_HEIGHT // 2) + (1.5 * line_height * (i - (len(lines) // 2)))
            ))

    def draw_health_bar(self, percent):
        """Draws player health bar. It consists of the background rectangle and other black one
        that covers it."""
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

        self.surface.blit(
            surface,
            (settings.SCREEN_WIDTH - (settings.HEALTH_BAR_WIDTH + 3 * settings.HEALTH_BAR_BORDER),
             0 + settings.HEALTH_BAR_BORDER))

    def draw_entity(self, entity):
        """Draws image of the entity to surface."""
        self.surface.blit(entity.image, (entity.rectangle.x, entity.rectangle.y))
