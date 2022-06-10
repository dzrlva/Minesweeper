"""Simple Point class module to handle int coordinates only."""
from random import randint


class Point:
    """Class that represents integer coordinates."""

    @staticmethod
    def __convert(val):
        """Convert value to Point class if needed."""
        return val if isinstance(val, Point) else Point(val)

    @staticmethod
    def random(start, end=None):
        """
        Return random coordinate in given range.

        Provided values converted to Point if needed
        By default start = Point(0, 0), end = value as Point
        Result is x = randint(start.x, end.x), y = randint(start.y, end.y)
        """
        if end is None:
            start, end = 0, start
        start, end = Point.__convert(start), Point.__convert(end)
        if start.x >= end.x:
            raise ValueError('Start x cannot be greater than end x')
        if start.y >= end.y:
            raise ValueError('Start y cannot be greater than end y')
        x = randint(start.x, end.x - 1)
        y = randint(start.y, end.y - 1)
        return Point(x, y)

    @staticmethod
    def range(start, end=None, step=None):
        """
        Return range for coordinates.

        Provided values convert to Point if needed
        By default start = Point(0, 0), end = value as Point, step = Point(1, 1)
        Result - all coordinates of a square with certain step
        """
        if end is None:
            start, end = 0, start
        if step is None:
            step = 1
        start, end, step = map(Point.__convert, [start, end, step])
        if start.x > end.x:
            raise ValueError('Start x cannot be greater than end x')
        if start.y > end.y:
            raise ValueError('Start y cannot be greater than end y')
        for x in range(start.x, end.x, step.x):
            for y in range(start.y, end.y, step.y):
                yield Point(x, y)

    def __init__(self, val, y=None):
        """
        Create Point instance.

        Takes one or two parameters
        If only one value is present assuming following:
        * Point                  -> just a copy
        * list/tuple length of 2 -> Point(val[0], val[1])
        * dict with 'x' and 'y'  -> Point(val['x'], val['y'])
        * int/float              -> Point(val, val)
        All values converted to int
        If both arguments are given, assuming they are numbers:
        Point(val, y), both converted to int
        """
        if y is None:
            if isinstance(val, Point):
                self.x, self.y = val.x, val.y

            elif isinstance(val, tuple) or isinstance(val, list):
                if len(val) != 2:
                    raise ValueError('Cannot convert list/tuple to Point with length != 2')
                self.x, self.y = int(val[0]), int(val[1])

            elif isinstance(val, dict) and 'x' in val and 'y' in val:
                self.x, self.y = int(val['x']), int(val['y'])

            elif isinstance(val, int) or isinstance(val, float):
                self.x, self.y = int(val), int(val)

            else:
                raise ValueError(f'Cannot convert type {type(val)} to Point')
        else:
            self.x, self.y = int(val), int(y)

    def __getitem__(self, idx):
        """Access x/y by 0/1 or a string."""
        if idx == 0 or idx == 'x':
            return self.x
        if idx == 1 or idx == 'y':
            return self.y

    def __setitem__(self, idx, val):
        """Set x/y by 0/1 or a string."""
        if idx == 0 or idx == 'x':
            self.x = int(val)
        if idx == 1 or idx == 'y':
            self.y = int(val)

    def __radd__(self, oth):
        """Addition of two Point, given value converted if needed."""
        val = Point.__convert(oth)
        return Point(val.x + self.x, val.y + self.y)

    def __rsub__(self, oth):
        """Addition of two Point, given value converted if needed."""
        val = Point.__convert(oth)
        return Point(val.x - self.x, val.y - self.y)

    def __sub__(self, oth):
        """Addition of two Point, given value converted if needed."""
        val = Point.__convert(oth)
        return Point(self.x - val.x, self.y - val.y)

    def __add__(self, oth):
        """Addition of two Point, given value converted if needed."""
        val = Point.__convert(oth)
        return Point(self.x + val.x, self.y + val.y)

    def __eq__(self, oth):
        """Addition of two Point, given value converted if needed."""
        val = Point.__convert(oth)
        return self.x == val.x and self.y == val.y

    def __iter__(self):
        """Return iterator for x and y values."""
        return iter((self.x, self.y))

    def __neg__(self):
        """Return negative of coords."""
        return Point(-self.x, -self.y)

    def __invert__(self):
        """Flip x and y places."""
        return Point(self.y, self.x)

    def __repr__(self):
        """Represent Point in console."""
        return f'Point <{self.x}, {self.y}>'

    def __str__(self):
        """Convert to string."""
        return f'({self.x}, {self.y})'

    def __hash__(self):
        return hash(f'({self.x},{self.y})')
