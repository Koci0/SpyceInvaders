import pygame

import SpyceInvaders.settings as settings
from SpyceInvaders.alien_group import AlienGroup
from SpyceInvaders.building import Building
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
        self.building_list = [
            Building(x=width // 4, y=height * (5 / 8)),
            Building(x=2 * width // 4, y=height * (5 / 8)),
            Building(x=3 * width // 4, y=height * (5 / 8))
        ]
        self.alien_group = AlienGroup()
        self.alien_bullets = []

    def run(self):
        running = True
        player_died = False
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
                    Bullet(self.player.rectangle.x + self.player.rectangle.width // 2, self.player.rectangle.y, "up"))

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
                        player_died = True
                        running = False
                    self.alien_bullets.remove(bullet)
                for building in self.building_list:
                    if bullet.is_collided_with(building):
                        building.receive_damage(10)
                        if not building.is_alive():
                            self.building_list.remove(building)
                        self.alien_bullets.remove(bullet)

            self.screen.draw_text("FPS: {:.0f}".format(self.clock.get_fps()))
            self.screen.draw_health_bar(self.player.hp)
            self.screen.draw_entity(self.player)
            for building in self.building_list:
                self.screen.draw_entity(building)
            for alien in self.alien_group.aliens:
                self.screen.draw_entity(alien)
            for bullet in self.player_bullets:
                self.screen.draw_entity(bullet)
            for bullet in self.alien_bullets:
                self.screen.draw_entity(bullet)

            pygame.display.flip()
            self.screen.surface.blit(self.screen.background, (0, 0))

        if player_died:
            self.count_quit()
        pygame.quit()

    def count_quit(self, text="You died!", time=3):
        self.screen.background.fill(settings.black)
        pygame.display.flip()
        self.screen.surface.blit(self.screen.background, (0, 0))
        print(text)
        print("Quiting in")
        for i in range(3, 0, -1):
            print(i)
            pygame.time.wait(1000)
        pygame.quit()
