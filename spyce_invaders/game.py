"""Defines in-game logic and mechanics."""

import pygame

from spyce_invaders import settings
from spyce_invaders.alien_group import AlienGroup
from spyce_invaders.building import Building
from spyce_invaders.leaderboard import Leaderboard
from spyce_invaders.player import Player
from spyce_invaders.screen import Screen


def is_collision_detected(source, target):
    """Detects if given source is collided with target.
    Returns target object if true, None otherwise."""
    if source.is_collided_with(target):
        return target
    return None


def handle_wait():
    """Waits for player to press any key or close window."""
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                done = True


class Game:
    """Creates screen object, starts clock, defines all actors and opens leaderboard."""
    width = settings.SCREEN_WIDTH
    height = settings.SCREEN_HEIGHT

    def __init__(self, fps=60):
        self.screen = Screen(self.width, self.height)
        self.clock = pygame.time.Clock()
        self.fps = fps

        self.player = None
        self.player_bullets = []
        self.building_list = []
        self.alien_group = None
        self.alien_bullets = []

        self.running = True
        self.next_level = True
        self.exit = False

        self.name = ""
        self.score = 0
        self.leaderboard = Leaderboard()

    def initialize_actors(self):
        """Initializes all actors in default starting positions."""
        self.player = Player(x=self.width // 2, y=self.height * (7 / 8))
        self.player_bullets = []
        self.building_list = [
            Building(x=(self.width - 4 * 60) // 5, y=self.height * (5 / 8)),
            Building(x=2 * (self.width - 4 * 60) // 5 + 1 * 60, y=self.height * (5 / 8)),
            Building(x=3 * (self.width - 4 * 60) // 5 + 2 * 60, y=self.height * (5 / 8)),
            Building(x=4 * (self.width - 4 * 60) // 5 + 3 * 60, y=self.height * (5 / 8))
        ]
        self.alien_group = AlienGroup()
        self.alien_bullets = []

    def run(self):
        """Runs game. For every level initializes actors and runs main game loop. When game is over,
        prompts player to input name, adds them to the leaderboard and prints it."""
        level = 1
        while self.next_level and not self.exit:
            self.level_screen("Level {}".format(level))
            self.initialize_actors()
            self.run_main_loop()
            level += 1

        if not self.exit:
            self.game_over_screen("GAME OVER")
            self.show_name_input()
            self.show_player_score()
            self.leaderboard.write_to_file(self.name, self.score)
            self.show_leaderboard()

    def run_main_loop(self):
        """Runs the main game loop. Handles game events, moves bullets, detects collisions,
        checks main conditions and draws actors. Stops when field running is set to False."""
        self.running = True
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

    def handle_events(self):
        """Handles closing window via X on window bar or escape key.
        Then checks if player should move or shoot."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.exit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    self.exit = True
                if event.key == pygame.K_n:
                    self.next_level = True
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
        """Checks if all aliens are dead, if all buildings are destroyed or
        if aliens touched the building."""
        if not self.alien_group.aliens:
            self.next_level = True
            self.running = False
            return
        if not self.building_list:
            self.next_level = False
            self.running = False
            return
        if not self.player.is_alive():
            self.next_level = False
            self.running = False
            return
        for building in self.building_list:
            for alien in self.alien_group.aliens:
                if is_collision_detected(alien, building):
                    self.next_level = False
                    self.running = False
                    return

    def detect_all_collisions(self):
        """Checks if player bullets touched aliens or buildings and
        if alien bullets touched player or buildings."""
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
        """Moves all bullets. If tick returns True, then bullet is out of screen
        and removes it from list."""
        for bullet in self.player_bullets:
            if bullet.tick():
                self.player_bullets.remove(bullet)
        for bullet in self.alien_bullets:
            if bullet.tick():
                self.alien_bullets.remove(bullet)

    def draw_all_actors(self):
        """Draws FPS text, score, health bar and all actors on screen."""
        self.screen.draw_text("FPS: {:.0f}".format(self.clock.get_fps()))
        self.screen.draw_text("Score: {}".format(self.score), y_coordinate=15)
        self.screen.draw_health_bar(self.player.health_points)
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

    def level_screen(self, text, seconds=1):
        """Draws given text in centered text for certain period of time in seconds."""
        self.screen.draw_center_text(text)
        self.screen.update_surface()
        pygame.time.wait(seconds * 1000)

    def game_over_screen(self, text):
        """Draws given text in centered text with prompt to press any key, then waits."""
        text.join("\n\nPress any key")
        self.screen.draw_center_text(text)
        self.screen.update_surface()

        handle_wait()

    def show_name_input(self):
        """Handles input of player name. Draws prompt and current input in centered text."""
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
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
        """Shows player score with prompt to press any key."""
        text = "Your score:\n{} {}\n\nPress any key".format(self.name, str(self.score))

        self.screen.draw_center_text(text)
        self.screen.update_surface()

        handle_wait()

    def show_leaderboard(self):
        """Shows leaderboard in centered text."""
        text = "Leaderboard\n"
        for line in self.leaderboard.read_from_file():
            text.join(line)
        text.join("\nPress any key")

        self.screen.draw_center_text(text)
        self.screen.update_surface()

        handle_wait()
