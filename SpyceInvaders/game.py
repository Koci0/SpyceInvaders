import pygame

from SpyceInvaders import settings
from SpyceInvaders.alien_group import AlienGroup
from SpyceInvaders.building import Building
from SpyceInvaders.leaderboard import Leaderboard
from SpyceInvaders.player import Player
from SpyceInvaders.screen import Screen


def is_collision_detected(source, target):
    if source.is_collided_with(target):
        return target
    return None


def handle_wait():
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                done = True


class Game:

    def __init__(self, width=settings.SCREEN_WIDTH, height=settings.SCREEN_HEIGHT, fps=60):
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
        self.player_won = False

        self.name = ""
        self.score = 0
        self.leaderboard = Leaderboard()

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
            self.check_game_over_conditions()
            self.draw_all_actors()

        if self.player_lost or self.player_won:
            if self.player_lost:
                self.game_over_screen("GAME OVER")
            elif self.player_won:
                self.game_over_screen("YOU WON")
            self.show_name_input()
            self.show_player_score()
            self.leaderboard.write_to_file(self.name, self.score)
            self.show_leaderboard()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player.move(settings.LEFT)
        elif keys[pygame.K_d]:
            self.player.move(settings.RIGHT)
        if keys[pygame.K_SPACE]:
            bullet = self.player.shoot(settings.UP)
            if bullet:
                self.player_bullets.append(bullet)

    def check_game_over_conditions(self):
        if not self.alien_group.aliens:
            self.player_won = True
            self.running = False
            return
        if not self.building_list:
            self.player_lost = True
            self.running = False
            return
        if not self.player.is_alive():
            self.player_lost = True
            self.running = False
            return
        for building in self.building_list:
            for alien in self.alien_group.aliens:
                if is_collision_detected(alien, building):
                    self.running = False
                    self.player_lost = True
                    return

    def detect_all_collisions(self):
        for bullet in self.player_bullets:
            for alien in self.alien_group.aliens:
                if is_collision_detected(bullet, alien):
                    self.alien_group.remove(alien)
                    self.player_bullets.remove(bullet)
                    self.score += alien.score
                    self.alien_group.increase_difficulty()

        for bullet in self.player_bullets:
            for building in self.building_list:
                if is_collision_detected(bullet, building):
                    building.receive_damage()
                    self.player_bullets.remove(bullet)
                    self.score -= building.score
                    if not building.is_alive():
                        self.building_list.remove(building)

        for bullet in self.alien_bullets:
            if is_collision_detected(bullet, self.player):
                self.player.receive_damage()
                self.alien_bullets.remove(bullet)

        for bullet in self.alien_bullets:
            for building in self.building_list:
                if is_collision_detected(bullet, building):
                    building.receive_damage()
                    self.alien_bullets.remove(bullet)

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
        self.screen.update_surface()

    def game_over_screen(self, text):
        text += "\n\nPress any key"
        self.screen.draw_center_text(text)
        self.screen.update_surface()

        handle_wait()

    def show_name_input(self):
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True
                    elif event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                    elif len(self.name) < settings.NAME_LENGTH:
                        self.name += event.unicode
            text = "Enter your name:\n{}".format(self.name)
            self.screen.draw_center_text(text)
            self.screen.update_surface()

    def show_player_score(self):
        text = "Your score:\n{} {}\n\nPress any key".format(self.name, str(self.score))

        self.screen.draw_center_text(text)
        self.screen.update_surface()

        handle_wait()

    def show_leaderboard(self):
        text = "Leaderboard\n"
        for line in self.leaderboard.read_from_file():
            text += line
        text += "\nPress any key"

        self.screen.draw_center_text(text)
        self.screen.update_surface()

        handle_wait()
