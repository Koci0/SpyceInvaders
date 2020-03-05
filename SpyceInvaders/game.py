import pygame

from SpyceInvaders.screen import Screen


class Game(object):

    def __init__(self, width=800, height=600, fps=60):
        self.screen = Screen(width, height)
        self.clock = pygame.time.Clock()
        self.fps = fps

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            self.clock.tick(self.fps)
            self.screen.draw_text("FPS: {:.0f}".format(self.clock.get_fps()))

            pygame.display.flip()
            self.screen.surface.blit(self.screen.background, (0, 0))

        pygame.quit()
