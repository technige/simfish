#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This module contains mock objects for testing both the tank environment
    and the contents individually. Tanks expose a minimal API to allow
    contained items to interact with them
"""

import simfish

class TestTank(object):
    """ Mock tank object for testing.
    """

    def __init__(self):
        self._items_with = []
        self.reset_movement_record()

    def reset_movement_record(self):
        self.last_item_moved = None
        self.total_dx = 0
        self.total_dy = 0

    def add_items_with(self, *items):
        self._items_with.extend(items)

    def items_with(self, item):
        return self._items_with

    def move(self, item, dx, dy):
        self.last_item_moved = item
        self.total_dx += dx
        self.total_dy += dy

    def remove(self, item):
        self._items_with.remove(item)


class TestFish(simfish.Mobile, simfish.Animal):
    """ Mock fish object for testing.
    """

    def __init__(self, direction=None, energy=120):
        simfish.Animal.__init__(self, energy=energy, diet=[simfish.FishFood])
        simfish.Mobile.__init__(self, direction, reversal=0.0, upward=0.0, downward=0.0)
        self.turns_taken = 0

    def turn(self, tank):
        self.turns_taken += 1
        if self.alive:
            self.breathe()
            self.eat(tank)
            self.swim(tank)
        else:
            self.float_(tank)
