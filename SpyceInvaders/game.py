import pygame

import SpyceInvaders.settings as settings
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
                for alien in self.alien_group.aliens:
                    if bullet.is_collided_with(alien):
                        alien.receive_damage(1)
                        if not alien.is_alive():
                            self.alien_group.remove(alien)
                        self.player_bullets.remove(bullet)

            for bullet in self.alien_bullets:
                if bullet.tick():
                    self.alien_bullets.remove(bullet)
                if bullet.is_collided_with(self.player):
                    self.player.receive_damage(10)
                    if not self.player.is_alive():
                        self.count_quit()
                        running = False
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

        pygame.quit()

    def count_quit(self, text="You died!", time=3):
        self.screen.background.fill(settings.black)
        self.screen.surface.blit(self.screen.background, (0, 0))
        print(text)
        print("Quiting in")
        for i in range(3, 0, -1):
            print(i)
            pygame.time.wait(1000)
        pygame.quit()
