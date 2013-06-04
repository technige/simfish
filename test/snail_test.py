#!/usr/bin/env python
# -*- coding: utf-8 -*-

import simfish
import unittest

from testutil import TestTank


class SnailTest(unittest.TestCase):

    def test_can_create(self):
        snail = simfish.Snail()
        self.assertTrue(snail.alive)
        self.assertEqual(simfish.Snail.ENERGY, snail.energy)
        self.assertEqual(1, len(snail.diet))
        self.assertTrue(simfish.FishFood in snail.diet)

    def test_can_breathe(self):
        tank = TestTank()
        snail = simfish.Snail()
        self.assertTrue(snail.alive)
        self.assertEqual(simfish.Snail.ENERGY, snail.energy)
        snail.turn(tank)
        self.assertEqual(simfish.Snail.ENERGY - 1, snail.energy)

    def test_can_die(self):
        tank = TestTank()
        snail = simfish.Snail()
        self.assertTrue(snail.alive)
        self.assertEqual(simfish.Snail.ENERGY, snail.energy)
        for i in range(simfish.Snail.ENERGY):
            snail.turn(tank)
        self.assertEqual(0, snail.energy)
        self.assertFalse(snail.alive)

    def test_will_eat_fish_food(self):
        tank = TestTank()
        others = [simfish.FishFood()]
        tank.add_items_with(*others)
        snail = simfish.Snail()
        self.assertEqual(others, tank.items_with(snail))
        snail.turn(tank)
        self.assertEqual(0, len(tank.items_with(snail)))

    def test_will_only_eat_one_fish_food_per_turn(self):
        FOOD_COUNT = 10
        tank = TestTank()
        others = [simfish.FishFood()] * FOOD_COUNT
        tank.add_items_with(*others)
        snail = simfish.Snail()
        for count in range(FOOD_COUNT, 0, -1):
            self.assertEqual(count, len(tank.items_with(snail)))
            snail.turn(tank)
        self.assertEqual(0, len(tank.items_with(snail)))

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
        snail = simfish.Snail()
        self.assertEqual(others, tank.items_with(snail))
        snail.turn(tank)
        self.assertEqual(others, tank.items_with(snail))

    def test_will_sink_when_dead(self):
        tank = TestTank()
        snail = simfish.Snail()
        for i in range(simfish.Snail.ENERGY):
            snail.turn(tank)
        self.assertFalse(snail.alive)
        tank.reset_movement_record()
        snail.turn(tank)
        self.assertEqual(snail, tank.last_item_moved)
        self.assertEqual(0, tank.total_dx)
        self.assertEqual(1, tank.total_dy)


if __name__ == "__main__":
    unittest.main()
