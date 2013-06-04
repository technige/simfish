#!/usr/bin/env python
# -*- coding: utf-8 -*-

import simfish
import unittest

from testutil import TestTank


class FishFoodTest(unittest.TestCase):

    def test_can_create(self):
        fish_food = simfish.FishFood()

    def test_has_correct_default_energy(self):
        fish_food = simfish.FishFood()
        self.assertEqual(10, fish_food.energy)

    def test_can_adjust_energy(self):
        fish_food = simfish.FishFood(energy=42)
        self.assertEqual(42, fish_food.energy)

    def test_will_sink(self):
        tank = TestTank()
        fish_food = simfish.FishFood()
        fish_food.turn(tank)
        self.assertEqual(fish_food, tank.last_item_moved)
        self.assertEqual(0, tank.total_dx)
        self.assertEqual(1, tank.total_dy)


if __name__ == "__main__":
    unittest.main()
