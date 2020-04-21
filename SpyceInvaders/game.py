import pygame

import SpyceInvaders.settings as settings
from SpyceInvaders.alien_group import AlienGroup
from SpyceInvaders.building import Building
from SpyceInvaders.player import Player
from SpyceInvaders.screen import Screen


class Game(object):

    def __init__(self, width=settings.screen_width, height=settings.screen_height, fps=60):
        self.screen = Screen(width, height)
        self.clock = pygame.time.Clock()
        self.fps = fps

        self.player = Player(x=width // 2, y=height * (7 / 8))
        self.player_bullets = []
        self.building_list = [
            Building(x=(width - 4 * 60) // 5, y=height * (5 / 8)),
            Building(x=2 * (width - 4 * 60) // 5 + 1 * 60, y=height * (5 / 8)),
            Building(x=3 * (width - 4 * 60) // 5 + 2 * 60, y=height * (5 / 8)),
            Building(x=4 * (width - 4 * 60) // 5 + 3 * 60, y=height * (5 / 8))
        ]
        self.alien_group = AlienGroup()
        self.alien_bullets = []

        self.running = True
        self.player_lost = False

    def run(self):
        while self.running:
            self.handle_events()
            self.clock.tick(self.fps)

            # Move all aliens and check for spawned bullets
            alien_bullet = self.alien_group.tick()
            if alien_bullet:
                self.alien_bullets.append(alien_bullet)

            self.move_all_bullets()
            self.detect_all_collisions()
            self.draw_all_actors()

        if self.player_lost:
            self.game_over_screen()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player.move("left")
        elif keys[pygame.K_d]:
            self.player.move("right")
        if keys[pygame.K_SPACE]:
            bullet = self.player.shoot("up")
            if bullet:
                self.player_bullets.append(bullet)

    def detect_all_collisions(self):
        for bullet in self.player_bullets:
            for alien in self.alien_group.aliens:
                if self.is_collision_detected(bullet, alien):
                    self.alien_group.remove(alien)
                    self.player_bullets.remove(bullet)
                    self.alien_group.increase_difficulty()

        for bullet in self.player_bullets:
            for building in self.building_list:
                if self.is_collision_detected(bullet, building):
                    building.receive_damage(bullet)
                    self.player_bullets.remove(bullet)
        for bullet in self.alien_bullets:
            if self.is_collision_detected(bullet, self.player):
                self.player.receive_damage(bullet)
                self.alien_bullets.remove(bullet)
                if not self.player.is_alive():
                    self.player_lost = True
                    self.running = False

        for bullet in self.alien_bullets:
            for building in self.building_list:
                if self.is_collision_detected(bullet, building):
                    building.receive_damage(bullet)
                    self.alien_bullets.remove(bullet)

        for building in self.building_list:
            for alien in self.alien_group.aliens:
                if self.is_collision_detected(alien, building):
                    self.running = False
                    self.player_lost = True

    def is_collision_detected(self, source, target):
        if source.is_collided_with(target):
            return target
        return None

    def move_all_bullets(self):
        for bullet in self.player_bullets:
            if bullet.tick():
                self.player_bullets.remove(bullet)
        for bullet in self.alien_bullets:
            if bullet.tick():
                self.alien_bullets.remove(bullet)

    def draw_all_actors(self):
        self.screen.draw_text("FPS: {:.0f}".format(self.clock.get_fps()))
        self.screen.draw_health_bar(self.player.hp)
        self.screen.draw_entity(self.player)
        for building in self.building_list:
            self.screen.draw_building(building)
        for alien in self.alien_group.aliens:
            self.screen.draw_entity(alien)
        for bullet in self.player_bullets:
            self.screen.draw_entity(bullet)
        for bullet in self.alien_bullets:
            self.screen.draw_entity(bullet)
        self.screen.update_surface()

    def game_over_screen(self, time=3):
        self.screen.draw_center_text("GAME OVER")
        self.screen.update_surface()
        for _ in range(time):
            pygame.time.wait(1000)
        pygame.quit()
