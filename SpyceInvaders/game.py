import pygame

from SpyceInvaders.bullet import Bullet
from SpyceInvaders.player import Player
from SpyceInvaders.screen import Screen


class Game(object):

    def __init__(self, width=800, height=600, fps=60):
        self.screen = Screen(width, height)
        self.clock = pygame.time.Clock()
        self.fps = fps

        self.player = Player(x=width // 2, y=height * (7 / 8))
        self.bullets = []

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
            if keys[pygame.K_SPACE]:
                self.bullets.append(
                    Bullet(self.player.x + self.player.rectangle.width // 2, self.player.y, "up"))

            self.clock.tick(self.fps)

            for bullet in self.bullets:
                if bullet.tick():
                    self.bullets.remove(bullet)

            self.screen.draw_text("FPS: {:.0f}".format(self.clock.get_fps()))
            self.screen.draw_entity(self.player)
            for bullet in self.bullets:
                self.screen.draw_entity(bullet)

            pygame.display.flip()
            self.screen.surface.blit(self.screen.background, (0, 0))
            print("#bullets = {}".format(len(self.bullets)))

        pygame.quit()
