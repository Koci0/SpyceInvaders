"""Tests for Actor module."""

import unittest

import pygame

from spyce_invaders import settings
from spyce_invaders.actor import Actor
from spyce_invaders.screen import Screen


class DamageTest(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = Screen()
        self.entity = Actor("test.png", 0, 0)
        self.entity.destructible = True

    def test_indestructible(self):
        self.entity.destructible = False
        self.entity.health_points = 100
        self.entity.receive_damage()
        self.assertEqual(self.entity.health_points, 100)

    def test_receive_damage(self):
        self.entity.health_points = 100
        self.entity.receive_damage()
        self.assertEqual(self.entity.health_points, 100 - settings.BULLET_DAMAGE)

    def test_die(self):
        self.entity.health_points = 1
        self.entity.receive_damage()
        self.assertFalse(self.entity.is_alive())


if __name__ == "__main__":
    unittest.main()
