#!/usr/bin/env python
# -*- coding: utf-8 -*-

import simfish
import unittest

from testutil import TestTank


class ClockworkFishTest(unittest.TestCase):

    def test_will_not_eat_fish_food(self):
        tank = TestTank()
        others = [simfish.FishFood()]
        tank.add_items_with(*others)
        clockwork_fish = simfish.ClockworkFish()
        self.assertEqual(others, tank.items_with(clockwork_fish))
        clockwork_fish.turn(tank)
        self.assertEqual(others, tank.items_with(clockwork_fish))

    def test_will_not_eat_other_creatures(self):
        tank = TestTank()
        others = [
            simfish.Snail(),
            simfish.SunFish(),
            simfish.DiverFish(),
            simfish.PiranhaFish(),
            simfish.ClockworkFish(),
        ]
        tank.add_items_with(*others)
        clockwork_fish = simfish.ClockworkFish()
        self.assertEqual(others, tank.items_with(clockwork_fish))
        clockwork_fish.turn(tank)
        self.assertEqual(others, tank.items_with(clockwork_fish))


if __name__ == "__main__":
    unittest.main()
