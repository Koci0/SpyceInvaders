import pygame

from SpyceInvaders.screen import Screen
from SpyceInvaders.player import Player


class Game(object):

    def __init__(self, width=800, height=600, fps=60):
        self.screen = Screen(width, height)
        self.clock = pygame.time.Clock()
        self.fps = fps

        self.player = Player("player", width//2, height*(7/8))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.player.move("left")
            elif keys[pygame.K_d]:
                self.player.move("right")

            self.clock.tick(self.fps)
            self.screen.draw_text("FPS: {:.0f}".format(self.clock.get_fps()))
            self.screen.draw_entity(self.player)

            pygame.display.flip()
            self.screen.surface.blit(self.screen.background, (0, 0))

        pygame.quit()
