import sys

import pygame

black = (0, 0, 0)
white = (255, 255, 255)


class View(object):

    def __init__(self, width=800, height=400, fps=60):
        pygame.init()
        pygame.display.set_caption("Press ESC to quit")
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill(black)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.font = pygame.font.SysFont("mono", 24)

    def paint(self):
        pygame.draw.rect(self.background, white, (200, 150, 50, 50))

    def run(self):
        self.paint()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            self.clock.tick(self.fps)
            self.draw_text("FPS: {:6.3}".format(self.clock.get_fps()))

            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))

        pygame.quit()

    def draw_text(self, text):
        fw, fh = self.font.size(text)
        surface = self.font.render(text, True, white)
        self.screen.blit(surface, (0, 0))


def run():
    View().run()
    sys.exit()
