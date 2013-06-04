#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Fish tank simulator
"""

import curses
import random
import time

TANK_WIDTH  = 15
TANK_HEIGHT = 10
UNIT_WIDTH  = 5
UNIT_HEIGHT = 2

EAST = +1
WEST = -1


class EdgeOfTank(Exception):

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class Tank(object):
    """ The tank is the environment in which the aquatic life lives. The
        details of the items themselves is unimportant except that each item
        must implement a `sprite` property and a `turn` method. All such
        items should generally inherit from the `Tank`.`Item` class.
    """

    class Item(object):
        """ Base class for items to be contained within a tank.
        """

        def __init__(self):
            pass

        @property
        def sprite(self):
            """ Return an ASCII art sprite to be drawn on the screen as a list
                of lines of text. Each line will be drawn below the previous
                line and the overall size should adhere to the `UNIT_WIDTH`
                and `UNIT_HEIGHT` variables defined at module level.
            """
            return ["     ",
                    "     "]

        def turn(self, tank):
            """ Take any required actions for a single time period or cycle.
                This method should be implemented for all subclasses and will
                be called for each iteration of the tank environment.

                :param tank: the tank environment in which this turn is taken
            """
            pass

        def sink(self, tank):
            """ Attempt to move the item downwards within the tank provided.
            """
            try:
                tank.move(self, 0, 1)
            except EdgeOfTank:
                pass

        def float_(self, tank):
            """ Attempt to move the item upwards within the tank provided.
            """
            try:
                tank.move(self, 0, -1)
            except EdgeOfTank:
                pass

    def __init__(self, temperature=17.0, window=None):
        """ Create a new tank to be displayed on the curses window supplied.

            :param window: a curses window on which to display the tank
        """
        self._temperature = temperature
        self.window = window
        self.width = TANK_WIDTH
        self.height = TANK_HEIGHT
        self.empty()

    def __len__(self):
        """ Return the number of items resident in this tank.
        """
        tally = 0
        for items in self._items.values():
            tally += len(items)
        return tally

    def remove_dead(self):
        for coords, items in self._items.items():
            death_list = []
            for item in items:
                if isinstance(item, Animal) and not item.alive:
                    death_list.append(item)
            for creature in death_list:
                items.remove(creature)

    def empty(self):
        """ Remove all the items from the tank to empty it.
            The `_items` dictionary holds a mapping of all (x, y) co-ordinates
            to a list of the items contained at that location. For example:
            {
                 (2, 4): [<Snail object>],
                 (10, 1): [<Food object>, <SunFish object>]
            }
        """
        self._items = {}

    def put(self, item, x=None, y=None):
        """ Place the item provided within the tank. If provided, use the x and
            y co-ordinates supplied, otherwise place at the top of the tank at
            a random horizontal position.
        """
        if x is None:
            x = random.randint(0, self.width - 1)
        if y is None:
            y = 0
        self.remove(item)
        if (x, y) in self._items:
            self._items[(x, y)].append(item)
        else:
            self._items[(x, y)] = [item]

    def remove(self, item):
        """ Remove the item provided from the tank.
        """
        empties = []
        for coords, items in self._items.items():
            if item in items:
                items.remove(item)
                if not items:
                    empties.append(coords)
                break
        for empty in empties:
            del self._items[empty]

    def items_with(self, item):
        """ Fetch a list of all items which overlap the item provided.
        """
        for items in self._items.values():
            if item in items:
                other_items = items[:]
                other_items.remove(item)
                return other_items
        return []

    def move(self, item, dx, dy):
        """ Move the item provided by the horizontal and vertical amounts
            supplied within `dx` and `dy` respectively.
        """
        for (x, y), items in self._items.items():
            if item in items:
                x += dx
                y += dy
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.put(item, x, y)
                    return
                else:
                    raise EdgeOfTank()
        raise ValueError("Item not found in fish tank")

    def warm(self):
        """ Increase the tank temperature by 0.1 degrees.
        """
        self._temperature += 0.1

    def cool(self):
        """ Decrease the tank temperature by 0.1 degrees.
        """
        self._temperature -= 0.1

    def temperature(self):
        """ Return the current tank temperature.
        """
        return self._temperature

    def turn(self):
        """ Iterate a single cycle of the items within the tank. Also
            provides random temperature variation.
        """
        for coords, items in self._items.items():
            for item in items:
                item.turn(self)
        n = random.random()
        if self._temperature > 15.0:
            if n < 0.3:
                self.cool()
            elif n >= 0.8:
                self.warm()
        else:
            if n < 0.2:
                self.cool()
            elif n >= 0.7:
                self.warm()

    def draw(self):
        """ Draw the tank to the window supplied on construction.
        """
        if self.window is None:
            return
        self.window.erase()
        self.window.addstr(0, 0, "|" + UNIT_WIDTH * self.width * "~" + "|")
        for y in range(UNIT_HEIGHT * self.height):
            self.window.addstr(y + 1, 0, "|")
            self.window.addstr(y + 1, UNIT_WIDTH * self.width + 1, "|")
        self.window.addstr(UNIT_HEIGHT * self.height + 1, 0, "+" + UNIT_WIDTH * self.width * "-" + "+")
        for (x, y), items in self._items.items():
            if items:
                for i, line in enumerate(items[0].sprite):
                    self.window.addnstr(UNIT_HEIGHT * y + i + 1, UNIT_WIDTH * x + 1, line, UNIT_WIDTH)
        self.window.addstr(UNIT_HEIGHT * TANK_HEIGHT + 2, 0,
            "tank temperature is {0:.1f} degrees".format(self._temperature)
        )
        self.window.refresh()


class OrganicItem(Tank.Item):
    """ An OrganicItem is one which can contain some amount of energy and
        may be used as a food source.
    """

    def __init__(self, energy):
        """ Create a new OrganicItem with the initial energy level provided.
        """
        Tank.Item.__init__(self)
        self.energy = energy


class FishFood(OrganicItem):
    """ FishFood is an OrganicItem which has no purpose other than to provide
        energy to those creatures which consume it. FishFood is heavy and will
        naturally sink to the bottom of the tank it is in.
    """

    def __init__(self, energy=10):
        """ Create a new lump of FishFood containing the amount of energy
            provided.
        """
        OrganicItem.__init__(self, energy=energy)

    @property
    def sprite(self):
        return ["     ",
                " === "]

    def turn(self, tank):
        """ Each turn, FishFood will do nothing other than sink (until of
            course it's eaten!)
        """
        self.sink(tank)


class Animal(OrganicItem):
    """ An Animal is a form of OrganicItem which may also eat and breathe.
        Eating will increase the pool of energy available by the amount stored
        within the foodstuff consumed whereas breathing will deplete the
        energy pool by one unit each turn. Once all energy has been used up,
        the Animal dies.
    """

    def __init__(self, energy, diet):
        """ Create a new Animal with an initial energy pool of the size
            specified and a list of edible Item subtypes.
        """
        OrganicItem.__init__(self, energy)
        self.diet = diet

    @property
    def alive(self):
        """ Return true if the Animal is still alive (i.e. has remaining
            energy) or false otherwise.
        """
        return bool(self.energy)

    def kill(self):
        """ Kill this animal (set its energy to zero).
        """
        self.energy = 0

    def breathe(self):
        """ If alive, take a breath thereby reducing the energy available by
            one unit.
        """
        if self.alive:
            self.energy -= 1

    def eat(self, tank):
        """ Consume one item from the tank which is at the same location and
            is edible by this animal. If more than one such item exists, only
            one will be eaten per turn.
        """
        items = tank.items_with(self)
        for item in items:
            if isinstance(item, tuple(self.diet)):
                tank.remove(item)
                self.energy += item.energy
                # only one meal per turn
                break


class Mobile(object):
    """ Mobility is a trait which can be attributed to any Item, which may or
        may not be an Animal. This trait allows two functions, to swim and to
        explicitly reverse direction.
    """

    def __init__(self, direction=None, reversal=0.0, upward=0.0, downward=0.0):
        """ Initialise mobility, beginning in the direction provided (EAST or
            WEST). If no direction is provided, a random one is chosen. Values
            can also be provided which dictate the probabilities with which a
            random course alteration may occur, be that for `reversal` of
            direction or for `upward` or `downward` movement.
        """
        self.direction = direction or random.choice([EAST, WEST])
        self.reversal = reversal
        self.upward = upward
        self.downward = downward

    def reverse(self):
        """ Reverse the current direction of travel.
        """
        self.direction = -self.direction

    def swim(self, tank):
        """ Attempt to swim forwards within the Tank specified. If an
            EdgeOfTank exception is encountered then a reversal of direction
            is forced.
        """
        if random.random() < self.reversal:
            self.reverse()
            return
        try:
            n = random.random()
            if n < self.upward:
                tank.move(self, self.direction, -1)
            elif n >= 1.0 - self.downward:
                tank.move(self, self.direction, 1)
            else:
                tank.move(self, self.direction, 0)
        except EdgeOfTank:
            self.reverse()


class Snail(Mobile, Animal):

    ENERGY = 120

    def __init__(self, direction=None):
        Animal.__init__(self, energy=Snail.ENERGY, diet=[FishFood])
        Mobile.__init__(self, direction, reversal=0.1, upward=0.2, downward=0.2)

    @property
    def sprite(self):
        if self.direction < 0:
            if self.alive:
                return ["oo   ",
                        "[_(@)"]
            else:
                return ["xx   ",
                        "[_(@)"]
        else:
            if self.alive:
                return ["   oo",
                        "(@)_]"]
            else:
                return ["   xx",
                        "(@)_]"]

    def turn(self, tank):
        if self.alive:
            self.breathe()
            self.eat(tank)
            self.swim(tank)
        else:
            self.sink(tank)


class SunFish(Mobile, Animal):

    ENERGY = 300

    def __init__(self, direction=None):
        Animal.__init__(self, energy=SunFish.ENERGY, diet=[FishFood])
        Mobile.__init__(self, direction, reversal=0.1, upward=0.3, downward=0.1)

    @property
    def sprite(self):
        if self.direction < 0:
            if self.alive:
                return ["/o \\/",
                        ")__/\\"]
            else:
                return ["/  \\/",
                        "\\x_/\\"]
        else:
            if self.alive:
                return ["\\/ o\\",
                        "/\\__("]
            else:
                return ["\\/  \\",
                        "/\\_x/"]

    def turn(self, tank):
        if self.alive:
            self.breathe()
            self.eat(tank)
            self.swim(tank)
        else:
            self.float_(tank)


class DiverFish(Mobile, Animal):

    ENERGY = 180

    def __init__(self, direction=None):
        Animal.__init__(self, energy=DiverFish.ENERGY, diet=[FishFood])
        Mobile.__init__(self, direction, reversal=0.1, upward=0.1, downward=0.3)

    @property
    def sprite(self):
        if self.direction < 0:
            if self.alive:
                return ["/- \\/",
                        ")__/\\"]
            else:
                return ["/  \\/",
                        "\\x_/\\"]
        else:
            if self.alive:
                return ["\\/ -\\",
                        "/\\__("]
            else:
                return ["\\/  \\",
                        "/\\_x/"]

    def turn(self, tank):
        if self.alive:
            self.breathe()
            self.eat(tank)
            self.swim(tank)
        else:
            self.float_(tank)


class PiranhaFish(Mobile, Animal):

    ENERGY = 180

    def __init__(self, direction=None):
        Animal.__init__(self, energy=PiranhaFish.ENERGY, diet=[FishFood, SunFish, DiverFish])
        Mobile.__init__(self, direction, reversal=0.1, upward=0.2, downward=0.2)

    @property
    def sprite(self):
        if self.direction < 0:
            if self.alive:
                return ["/o \\/",
                        "::_/\\"]
            else:
                return [":: \\/",
                        "\\x_/\\"]
        else:
            if self.alive:
                return ["\\/ o\\",
                        "/\\_::"]
            else:
                return ["\\/ ::",
                        "/\\_x/"]

    def turn(self, tank):
        if self.alive:
            if tank.temperature() < 15.0:
                self.kill()
            else:
                self.breathe()
                self.eat(tank)
                self.swim(tank)
        else:
            self.float_(tank)


class ClockworkFish(Mobile, Tank.Item):
    """ ClockworkFish are Mobile but are not Animals. To that end, they swim
        around the tank like other fish but do not eat or breathe.
    """

    def __init__(self, direction=None):
        Tank.Item.__init__(self)
        Mobile.__init__(self, direction, reversal=0.0, upward=0.25, downward=0.25)

    @property
    def sprite(self):
        if self.direction < 0:
            return ["/+]\\/",
                    "\\__/\\"]
        else:
            return ["\\/[+\\",
                    "/\\__/"]

    def turn(self, tank):
        self.swim(tank)


def main(screen):
    """ The main game loop.
    """
    curses.curs_set(0)
    curses.halfdelay(10)
    tank = Tank(window=screen)
    running = True
    while running:
        while True:
            tank.draw()
            ch = screen.getch()
            if ch < 0:
                break
            elif ch == ord('s'):
                tank.put(SunFish())
            elif ch == ord('d'):
                tank.put(DiverFish())
            elif ch == ord('p'):
                tank.put(PiranhaFish())
            elif ch == ord('c'):
                tank.put(ClockworkFish())
            elif ch == ord('z'):
                tank.put(Snail())
            elif ch == ord('f'):
                tank.put(FishFood())
            elif ch == ord('['):
                tank.cool()
            elif ch == ord(']'):
                tank.warm()
            elif ch == ord('r'):
                tank.remove_dead()
            elif ch == ord('e'):
                tank.empty()
            elif ch == ord('q'):
                running = False
        if running:
            tank.turn()

if __name__ == "__main__":
    curses.wrapper(main)
