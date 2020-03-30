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

        self.running = True
        self.player_died = False

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

        if self.player_died:
            self.count_quit()
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
            self.player_bullets.append(
                Bullet(self.player.rectangle.x + self.player.rectangle.width // 2, self.player.rectangle.y, "up"))

    def detect_all_collisions(self):
        removed = self.detect_collision(self.alien_group.aliens, self.player_bullets)
        if removed is not None:
            self.alien_group.increase_difficulty()
        self.detect_collision(self.building_list, self.player_bullets)
        self.detect_collision([self.player], self.alien_bullets)
        self.detect_collision(self.building_list, self.alien_bullets)

    def detect_collision(self, targets, bullets):
        for bullet in bullets:
            for target in targets:
                if bullet.is_collided_with(target):
                    target.receive_damage(10)
                    if not target.is_alive():
                        if isinstance(target, Player):
                            self.player_died = True
                            self.running = False
                        else:
                            targets.remove(target)
                            return target
                    bullets.remove(bullet)
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
            self.screen.draw_entity(building)
        for alien in self.alien_group.aliens:
            self.screen.draw_entity(alien)
        for bullet in self.player_bullets:
            self.screen.draw_entity(bullet)
        for bullet in self.alien_bullets:
            self.screen.draw_entity(bullet)

        pygame.display.flip()
        self.screen.surface.blit(self.screen.background, (0, 0))

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
