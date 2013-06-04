#!/usr/bin/env python
# -*- coding: utf-8 -*-

import simfish
import unittest

from testutil import TestTank


class DiverFishTest(unittest.TestCase):

    def test_can_create(self):
        diver_fish = simfish.DiverFish()
        self.assertTrue(diver_fish.alive)
        self.assertEqual(simfish.DiverFish.ENERGY, diver_fish.energy)
        self.assertEqual(1, len(diver_fish.diet))
        self.assertTrue(simfish.FishFood in diver_fish.diet)

    def test_can_breathe(self):
        tank = TestTank()
        diver_fish = simfish.DiverFish()
        self.assertTrue(diver_fish.alive)
        self.assertEqual(simfish.DiverFish.ENERGY, diver_fish.energy)
        diver_fish.turn(tank)
        self.assertEqual(simfish.DiverFish.ENERGY - 1, diver_fish.energy)

    def test_can_die(self):
        tank = TestTank()
        diver_fish = simfish.DiverFish()
        self.assertTrue(diver_fish.alive)
        self.assertEqual(simfish.DiverFish.ENERGY, diver_fish.energy)
        for i in range(simfish.DiverFish.ENERGY):
            diver_fish.turn(tank)
        self.assertEqual(0, diver_fish.energy)
        self.assertFalse(diver_fish.alive)

    def test_will_eat_fish_food(self):
        tank = TestTank()
        others = [simfish.FishFood()]
        tank.add_items_with(*others)
        diver_fish = simfish.DiverFish()
        self.assertEqual(others, tank.items_with(diver_fish))
        diver_fish.turn(tank)
        self.assertEqual(0, len(tank.items_with(diver_fish)))

    def test_will_only_eat_one_fish_food_per_turn(self):
        FOOD_COUNT = 10
        tank = TestTank()
        others = [simfish.FishFood()] * FOOD_COUNT
        tank.add_items_with(*others)
        diver_fish = simfish.DiverFish()
        for count in range(FOOD_COUNT, 0, -1):
            self.assertEqual(count, len(tank.items_with(diver_fish)))
            diver_fish.turn(tank)
        self.assertEqual(0, len(tank.items_with(diver_fish)))

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
        diver_fish = simfish.DiverFish()
        self.assertEqual(others, tank.items_with(diver_fish))
        diver_fish.turn(tank)
        self.assertEqual(others, tank.items_with(diver_fish))

    def test_will_float_when_dead(self):
        tank = TestTank()
        diver_fish = simfish.DiverFish()
        for i in range(simfish.DiverFish.ENERGY):
            diver_fish.turn(tank)
        self.assertFalse(diver_fish.alive)
        tank.reset_movement_record()
        diver_fish.turn(tank)
        self.assertEqual(diver_fish, tank.last_item_moved)
        self.assertEqual(0, tank.total_dx)
        self.assertEqual(-1, tank.total_dy)


if __name__ == "__main__":
    unittest.main()
