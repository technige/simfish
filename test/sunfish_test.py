#!/usr/bin/env python
# -*- coding: utf-8 -*-

import simfish
import unittest

from testutil import TestTank


class SunFishTest(unittest.TestCase):

    def test_can_create(self):
        sun_fish = simfish.SunFish()
        self.assertTrue(sun_fish.alive)
        self.assertEqual(simfish.SunFish.ENERGY, sun_fish.energy)
        self.assertEqual(1, len(sun_fish.diet))
        self.assertTrue(simfish.FishFood in sun_fish.diet)

    def test_can_breathe(self):
        tank = TestTank()
        sun_fish = simfish.SunFish()
        self.assertTrue(sun_fish.alive)
        self.assertEqual(simfish.SunFish.ENERGY, sun_fish.energy)
        sun_fish.turn(tank)
        self.assertEqual(simfish.SunFish.ENERGY - 1, sun_fish.energy)

    def test_can_die(self):
        tank = TestTank()
        sun_fish = simfish.SunFish()
        self.assertTrue(sun_fish.alive)
        self.assertEqual(simfish.SunFish.ENERGY, sun_fish.energy)
        for i in range(simfish.SunFish.ENERGY):
            sun_fish.turn(tank)
        self.assertEqual(0, sun_fish.energy)
        self.assertFalse(sun_fish.alive)

    def test_will_eat_fish_food(self):
        tank = TestTank()
        others = [simfish.FishFood()]
        tank.add_items_with(*others)
        sun_fish = simfish.SunFish()
        self.assertEqual(others, tank.items_with(sun_fish))
        sun_fish.turn(tank)
        self.assertEqual(0, len(tank.items_with(sun_fish)))

    def test_will_only_eat_one_fish_food_per_turn(self):
        FOOD_COUNT = 10
        tank = TestTank()
        others = [simfish.FishFood()] * FOOD_COUNT
        tank.add_items_with(*others)
        sun_fish = simfish.SunFish()
        for count in range(FOOD_COUNT, 0, -1):
            self.assertEqual(count, len(tank.items_with(sun_fish)))
            sun_fish.turn(tank)
        self.assertEqual(0, len(tank.items_with(sun_fish)))

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
        sun_fish = simfish.SunFish()
        self.assertEqual(others, tank.items_with(sun_fish))
        sun_fish.turn(tank)
        self.assertEqual(others, tank.items_with(sun_fish))

    def test_will_float_when_dead(self):
        tank = TestTank()
        sun_fish = simfish.SunFish()
        for i in range(simfish.SunFish.ENERGY):
            sun_fish.turn(tank)
        self.assertFalse(sun_fish.alive)
        tank.reset_movement_record()
        sun_fish.turn(tank)
        self.assertEqual(sun_fish, tank.last_item_moved)
        self.assertEqual(0, tank.total_dx)
        self.assertEqual(-1, tank.total_dy)


if __name__ == "__main__":
    unittest.main()
