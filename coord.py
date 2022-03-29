from random import randint


class Coord:
    @staticmethod
    def __convert(val):
        return val if isinstance(val, Coord) else Coord(val)

    @staticmethod
    def random(start, end=None):
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
        if idx == 0 or idx == 'x':
            return self.x
        if idx == 1 or idx == 'y':
            return self.y

    def __setitem__(self, idx, val):
        if idx == 0 or idx == 'x':
            self.x = int(val)
        if idx == 1 or idx == 'y':
            self.y = int(val)

    def __radd__(self, oth):
        val = Coord.__convert(oth)
        return Coord(val.x + self.x, val.y + self.y)

    def __rsub__(self, oth):
        val = Coord.__convert(oth)
        return Coord(val.x - self.x, val.y - self.y)

    def __sub__(self, oth):
        val = Coord.__convert(oth)
        return Coord(self.x - val.x, self.y - val.y)

    def __add__(self, oth):
        val = Coord.__convert(oth)
        return Coord(self.x + val.x, self.y + val.y)

    def __eq__(self, oth):
        val = Coord.__convert(oth)
        return self.x == val.x and self.y == val.y

    def __iter__(self):
        return iter((self.x, self.y))

    def __neg__(self):
        return Coord(-self.x, -self.y)

    def __invert__(self):
        return Coord(self.y, self.x)

    def __repr__(self):
        return f'Coord <{self.x}, {self.y}>'

    def __str__(self):
        return f'({self.x}, {self.y})'
