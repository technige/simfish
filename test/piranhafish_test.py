#!/usr/bin/env python
# -*- coding: utf-8 -*-

import simfish
import unittest

from testutil import TestTank


class PiranhaFishTest(unittest.TestCase):

    def test_can_create(self):
        piranha_fish = simfish.PiranhaFish()
        self.assertTrue(piranha_fish.alive)
        self.assertEqual(simfish.PiranhaFish.ENERGY, piranha_fish.energy)
        self.assertEqual(3, len(piranha_fish.diet))
        self.assertTrue(simfish.FishFood in piranha_fish.diet)
        self.assertTrue(simfish.SunFish in piranha_fish.diet)
        self.assertTrue(simfish.DiverFish in piranha_fish.diet)

    def test_can_breathe(self):
        tank = TestTank()
        piranha_fish = simfish.PiranhaFish()
        self.assertTrue(piranha_fish.alive)
        self.assertEqual(simfish.PiranhaFish.ENERGY, piranha_fish.energy)
        piranha_fish.turn(tank)
        self.assertEqual(simfish.PiranhaFish.ENERGY - 1, piranha_fish.energy)

    def test_can_die(self):
        tank = TestTank()
        piranha_fish = simfish.PiranhaFish()
        self.assertTrue(piranha_fish.alive)
        self.assertEqual(simfish.PiranhaFish.ENERGY, piranha_fish.energy)
        for i in range(simfish.PiranhaFish.ENERGY):
            piranha_fish.turn(tank)
        self.assertEqual(0, piranha_fish.energy)
        self.assertFalse(piranha_fish.alive)

    def test_will_only_eat_one_item_per_turn(self):
        tank = TestTank()
        others = [simfish.FishFood(), simfish.SunFish(), simfish.DiverFish()]
        tank.add_items_with(*others)
        piranha_fish = simfish.PiranhaFish()
        for count in range(len(others), 0, -1):
            self.assertEqual(count, len(tank.items_with(piranha_fish)))
            piranha_fish.turn(tank)
        self.assertEqual(0, len(tank.items_with(piranha_fish)))

    def test_will_eat_fish_food(self):
        tank = TestTank()
        others = [simfish.FishFood()]
        tank.add_items_with(*others)
        piranha_fish = simfish.PiranhaFish()
        self.assertEqual(others, tank.items_with(piranha_fish))
        piranha_fish.turn(tank)
        self.assertEqual(0, len(tank.items_with(piranha_fish)))

    def test_will_eat_sun_fish(self):
        tank = TestTank()
        others = [simfish.SunFish()]
        tank.add_items_with(*others)
        piranha_fish = simfish.PiranhaFish()
        self.assertEqual(others, tank.items_with(piranha_fish))
        piranha_fish.turn(tank)
        self.assertEqual(0, len(tank.items_with(piranha_fish)))

    def test_will_eat_diver_fish(self):
        tank = TestTank()
        others = [simfish.DiverFish()]
        tank.add_items_with(*others)
        piranha_fish = simfish.PiranhaFish()
        self.assertEqual(others, tank.items_with(piranha_fish))
        piranha_fish.turn(tank)
        self.assertEqual(0, len(tank.items_with(piranha_fish)))

    def test_will_not_eat_snails(self):
        tank = TestTank()
        others = [simfish.Snail()]
        tank.add_items_with(*others)
        piranha_fish = simfish.PiranhaFish()
        self.assertEqual(others, tank.items_with(piranha_fish))
        piranha_fish.turn(tank)
        self.assertEqual(others, tank.items_with(piranha_fish))

    def test_will_not_eat_clockwork_fish(self):
        tank = TestTank()
        others = [simfish.ClockworkFish()]
        tank.add_items_with(*others)
        piranha_fish = simfish.PiranhaFish()
        self.assertEqual(others, tank.items_with(piranha_fish))
        piranha_fish.turn(tank)
        self.assertEqual(others, tank.items_with(piranha_fish))

    def test_will_float_when_dead(self):
        tank = TestTank()
        piranha_fish = simfish.PiranhaFish()
        for i in range(simfish.PiranhaFish.ENERGY):
            piranha_fish.turn(tank)
        self.assertFalse(piranha_fish.alive)
        tank.reset_movement_record()
        piranha_fish.turn(tank)
        self.assertEqual(piranha_fish, tank.last_item_moved)
        self.assertEqual(0, tank.total_dx)
        self.assertEqual(-1, tank.total_dy)


if __name__ == "__main__":
    unittest.main()
