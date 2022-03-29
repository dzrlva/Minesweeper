"""Simple Coord class module."""
from random import randint


class Coord:
    @staticmethod
    def __convert(val):
        """Converts value to Coord class if needed."""
        return val if isinstance(val, Coord) else Coord(val)

    @staticmethod
    def random(start, end=None):
        """
        Generats random coordinate in provided range
        Provided values converted to Coord if needed
        By default start = Coord(0, 0), end = value as Coord
        Result is x = randint(start.x, end.x), y = randint(start.y, end.y)
        """
        if end is None:
            start, end = 0, start
        start, end = Coord.__convert(start), Coord.__convert(end)
        if start.x > end.x:
            raise ValueError('Start x cannot be greater than end x')
        if start.y > end.y:
            raise ValueError('Start y cannot be greater than end y')
        x = randint(start.x, end.x)
        y = randint(start.y, end.y)
        return Coord(x, y)

    @staticmethod
    def range(start, end=None, step=None):
        """
        Generates range for coordinates
        Provided values convert to Coord if needed
        By default start = Coord(0, 0), end = value as Coord, step = Coord(1, 1)
        Result - all coordinates of a square with certain step
        """
        if end is None:
            start, end = 0, start
        if step is None:
            step = 1
        start, end, step = map(Coord.__convert, [start, end, step])
        if start.x > end.x:
            raise ValueError('Start x cannot be greater than end x')
        if start.y > end.y:
            raise ValueError('Start y cannot be greater than end y')
        for x in range(start.x, end.x, step.x):
            for y in range(start.y, end.y, step.y):
                yield Coord(x, y)

    def __init__(self, val, y=None):
        """
        Creates Coord instance
        Takes one or two parameters
        If only one value is present assuming following:
        * Coord                  -> just a copy
        * list/tuple length of 2 -> Coord(val[0], val[1])
        * dict with 'x' and 'y'  -> Coord(val['x'], val['y'])
        * int/float              -> Coord(val, val)
        All values converted to int
        If both arguments are given, assuming they are numbers:
        Coord(val, y), both converted to int
        """
        if y is None:
            if isinstance(val, Coord):
                self.x, self.y = val.x, val.y
            elif isinstance(val, tuple) or isinstance(val, list):
                if len(val) != 2:
                    raise ValueError('Cannot convert list/tuple to Coord with length != 2')
                self.x, self.y = int(val[0]), int(val[1])
            elif isinstance(val, dict) and 'x' in val and 'y' in val:
                self.x, self.y = int(val['x']), int(val['y'])
            elif isinstance(val, int) or isinstance(val, float):
                self.x, self.y = int(val), int(val)
            else:
                raise ValueError(f'Cannot convert type {type(val)} to Coord')
        else:
            self.x, self.y = int(val), int(y)

    def __getitem__(self, idx):
        """Allows to access x/y by 0/1 or a string."""
        if idx == 0 or idx == 'x':
            return self.x
        if idx == 1 or idx == 'y':
            return self.y

    def __setitem__(self, idx, val):
        """Allows to set x/y by 0/1 or a string."""
        if idx == 0 or idx == 'x':
            self.x = int(val)
        if idx == 1 or idx == 'y':
            self.y = int(val)

    def __radd__(self, oth):
        """Addition of two Coord, given value converted if needed."""
        val = Coord.__convert(oth)
        return Coord(val.x + self.x, val.y + self.y)

    def __rsub__(self, oth):
        """Addition of two Coord, given value converted if needed."""
        val = Coord.__convert(oth)
        return Coord(val.x - self.x, val.y - self.y)

    def __sub__(self, oth):
        """Addition of two Coord, given value converted if needed."""
        val = Coord.__convert(oth)
        return Coord(self.x - val.x, self.y - val.y)

    def __add__(self, oth):
        """Addition of two Coord, given value converted if needed."""
        val = Coord.__convert(oth)
        return Coord(self.x + val.x, self.y + val.y)

    def __eq__(self, oth):
        """Addition of two Coord, given value converted if needed."""
        val = Coord.__convert(oth)
        return self.x == val.x and self.y == val.y

    def __iter__(self):
        """Returns iterator for x and y values."""
        return iter((self.x, self.y))

    def __neg__(self):
        """Returns negative of coords."""
        return Coord(-self.x, -self.y)

    def __invert__(self):
        """Flips x and y places."""
        return Coord(self.y, self.x)

    def __repr__(self):
        """Represents Coord in console."""
        return f'Coord <{self.x}, {self.y}>'

    def __str__(self):
        """String converter."""
        return f'({self.x}, {self.y})'
