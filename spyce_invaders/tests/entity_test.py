"""Tests for Entity module."""

import unittest

import pygame

from spyce_invaders import settings
from spyce_invaders.entity import Entity
from spyce_invaders.screen import Screen


class MovementTest(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = Screen()
        self.entity = Entity("test.png", 0, 0)

    def test_left_bound(self):
        self.entity.rectangle.x = 0
        self.entity.move(settings.LEFT, 10)
        self.assertEqual(self.entity.rectangle.x, 0)

    def test_right_bound(self):
        self.entity.rectangle.x = settings.SCREEN_WIDTH - self.entity.rectangle.width - 1
        self.entity.move(settings.RIGHT, 10)
        self.assertEqual(self.entity.rectangle.x, settings.SCREEN_WIDTH - self.entity.rectangle.width - 1)

    def test_upper_bound(self):
        self.entity.rectangle.y = 0
        self.entity.move(settings.UP, 10)
        self.assertEqual(self.entity.rectangle.y, 0)

    def test_lower_bound(self):
        self.entity.rectangle.y = settings.SCREEN_HEIGHT - self.entity.rectangle.height - 1
        self.entity.move(settings.DOWN, 10)
        self.assertEqual(self.entity.rectangle.y, settings.SCREEN_HEIGHT - self.entity.rectangle.height - 1)


if __name__ == "__main__":
    unittest.main()
