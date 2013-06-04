#!/usr/bin/env python
# -*- coding: utf-8 -*-

import simfish
import unittest

from testutil import TestFish


class TankTest(unittest.TestCase):

    def test_can_put_items_in_tank(self):
        tank = simfish.Tank(None)
        for i in range(1, 100):
            tank.put(TestFish(), x=0, y=0)
            self.assertEqual(i, len(tank))

    def test_can_remove_items_from_tank(self):
        tank = simfish.Tank(None)
        fish = TestFish()
        tank.put(fish, x=0, y=0)
        self.assertEqual(1, len(tank))
        tank.remove(fish)
        self.assertEqual(0, len(tank))

    def test_can_identify_overlapping_items(self):
        tank = simfish.Tank(None)
        fishes = [TestFish(), TestFish(), TestFish()]
        for fish in fishes:
            tank.put(fish, x=0, y=0)
        other_fish = tank.items_with(fishes[0])
        self.assertEqual(2, len(other_fish))
        self.assertFalse(fishes[0] in other_fish)
        self.assertTrue(fishes[1] in other_fish)
        self.assertTrue(fishes[2] in other_fish)
        other_fish = tank.items_with(fishes[1])
        self.assertEqual(2, len(other_fish))
        self.assertTrue(fishes[0] in other_fish)
        self.assertFalse(fishes[1] in other_fish)
        self.assertTrue(fishes[2] in other_fish)
        other_fish = tank.items_with(fishes[2])
        self.assertEqual(2, len(other_fish))
        self.assertTrue(fishes[0] in other_fish)
        self.assertTrue(fishes[1] in other_fish)
        self.assertFalse(fishes[2] in other_fish)

    def test_can_move_items(self):
        tank = simfish.Tank(None)
        fishes = [TestFish(), TestFish(), TestFish()]
        tank.put(fishes[0], x=0, y=0)
        tank.put(fishes[1], x=0, y=0)
        tank.put(fishes[2], x=1, y=1)
        other_fish = tank.items_with(fishes[0])
        self.assertEqual(1, len(other_fish))
        self.assertTrue(fishes[1] in other_fish)
        self.assertFalse(fishes[2] in other_fish)
        tank.move(fishes[0], dx=1, dy=1)
        other_fish = tank.items_with(fishes[0])
        self.assertEqual(1, len(other_fish))
        self.assertFalse(fishes[1] in other_fish)
        self.assertTrue(fishes[2] in other_fish)

    def test_can_take_turns(self):
        tank = simfish.Tank(None)
        fish = TestFish()
        tank.put(fish, x=0, y=0)
        for i in range(10):
            self.assertEqual(i, fish.turns_taken)
            tank.turn()
        self.assertEqual(10, fish.turns_taken)


if __name__ == "__main__":
    unittest.main()
