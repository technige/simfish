#!/usr/bin/env python
# -*- coding: utf-8 -*-

import simfish
import unittest

from testutil import TestTank, TestFish


class MobilityTest(unittest.TestCase):

    def test_can_create_mobile_object(self):
        fish = TestFish(direction=simfish.EAST)
        self.assertEqual(simfish.EAST, fish.direction)
        self.assertEqual(0.0, fish.reversal)
        self.assertEqual(0.0, fish.upward)
        self.assertEqual(0.0, fish.downward)

    def test_can_reverse_direction_east_to_west(self):
        fish = TestFish(direction=simfish.EAST)
        fish.reverse()
        self.assertEqual(simfish.WEST, fish.direction)
        self.assertEqual(0.0, fish.reversal)
        self.assertEqual(0.0, fish.upward)
        self.assertEqual(0.0, fish.downward)

    def test_can_reverse_direction_west_to_east(self):
        fish = TestFish(direction=simfish.WEST)
        fish.reverse()
        self.assertEqual(simfish.EAST, fish.direction)
        self.assertEqual(0.0, fish.reversal)
        self.assertEqual(0.0, fish.upward)
        self.assertEqual(0.0, fish.downward)

    def test_will_swim_forward(self):
        tank = TestTank()
        fish = TestFish(direction=simfish.EAST)
        tank.reset_movement_record()
        for i in range(fish.energy):
            fish.turn(tank)
            self.assertEqual(fish, tank.last_item_moved)
            self.assertEqual(i + 1, tank.total_dx)
            self.assertEqual(0, tank.total_dy)
        self.assertEqual(0, fish.energy)


if __name__ == "__main__":
    unittest.main()
