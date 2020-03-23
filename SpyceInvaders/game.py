import pygame

from SpyceInvaders.alien_group import AlienGroup
from SpyceInvaders.bullet import Bullet
from SpyceInvaders.player import Player
from SpyceInvaders.screen import Screen


class Game(object):

    def __init__(self, width=800, height=600, fps=60):
        self.screen = Screen(width, height)
        self.clock = pygame.time.Clock()
        self.fps = fps

        self.player = Player(x=width // 2, y=height * (7 / 8))
        self.player_bullets = []
        self.alien_group = AlienGroup()
        self.alien_bullets = []

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
                self.player_bullets.append(
                    Bullet(self.player.x + self.player.rectangle.width // 2, self.player.y, "up"))

            self.clock.tick(self.fps)

            alien_bullet = self.alien_group.tick()
            if alien_bullet:
                self.alien_bullets.append(alien_bullet)

            for bullet in self.player_bullets:
                if bullet.tick():
                    self.player_bullets.remove(bullet)
            for bullet in self.alien_bullets:
                if bullet.tick():
                    self.alien_bullets.remove(bullet)

            self.screen.draw_text("FPS: {:.0f}".format(self.clock.get_fps()))
            self.screen.draw_entity(self.player)
            for alien in self.alien_group.aliens:
                self.screen.draw_entity(alien)
            for bullet in self.player_bullets:
                self.screen.draw_entity(bullet)
            for bullet in self.alien_bullets:
                self.screen.draw_entity(bullet)

            pygame.display.flip()
            self.screen.surface.blit(self.screen.background, (0, 0))
            print("#bullets = player:{}, alien:{}".format(len(self.player_bullets), len(self.alien_bullets)))

        pygame.quit()
