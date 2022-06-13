"""Module for the Field class."""

from util import Point
from util.minepoint import MinePoint, Value, Mask, Flag


def NoramlPattern(point):
    """Pattern for rectangular minesweeper."""
    return [
        Point(-1, -1), Point(0, -1), Point(1, -1),
        Point(-1, 0), Point(1, 0),
        Point(-1, 1), Point(0, 1), Point(1, 1)
    ]


def HexagonPatter(point):
    """Pattern for Hexagonal minesweeper."""
    if point.y % 2 == 0:
        return [
            Point(0, -1), Point(1, -1),
            Point(-1, 0), Point(1, 0),
            Point(0, 1), Point(1, 1),
        ]
    else:
        return [
            Point(-1, -1), Point(0, -1),
            Point(-1, 0), Point(1, 0),
            Point(-1, 1), Point(0, 1),
        ]


class Field:
    """Logic for minesweeper minefield."""

    OUTOFBOUND = -1

    def __init__(self, width, height, bombsPercent, kind='normal'):
        """Initialize field with size and bombs. Randomly fill it."""
        if kind == 'normal':
            self.pattern = NoramlPattern
        elif kind == 'hexagon':
            self.pattern = HexagonPatter
        else:
            raise ValueError('Unkown kind of field pattern')

        self.size = width * height
        self.width, self.height = width, height
        self.bombs = round(self.size * bombsPercent)
        self.__field = [[MinePoint() for _ in range(width)]
                        for _ in range(height)]
        self.bombsPos = set()
        self.__randomizeBombs()
        self.__calcFieldBombs()

    def __isOutOfBounds(self, x, y=None):
        x, y = Point(x, y)
        return x < 0 or y < 0 or x >= self.width or y >= self.height

    def inBounds(self, x, y=None):
        """Return if point is in field bounds."""
        return not self.__isOutOfBounds(x, y)

    def __getitem__(self, coords):
        """Return field minepoint if in bound else OUTOFBOUND value."""
        x, y = Point(coords)
        if self.__isOutOfBounds(x, y):
            return Field.OUTOFBOUND
        return self.__field[y][x]

    def __setitem__(self, coords, value):
        """Set minepoint value if in bound."""
        x, y = Point(coords)
        if self.__isOutOfBounds(x, y):
            raise ValueError(f'Coords {coords} are out of bounds')

        if isinstance(value, Value):
            if value == Value.bomb:
                self.bombsPos.add(Point(x, y))
            elif self[x, y] == Value.bomb:
                self.bombsPos.remove(Point(x, y))
        self.__field[y][x].set(value)

    def __randomizeBombs(self):
        """Randomize bomb position."""
        for _ in range(self.bombs):
            x, y = Point.random([self.width, self.height])
            while self[x, y] == Value.bomb:
                x, y = Point.random([self.width, self.height])
            self[x, y] = Value.bomb

    def __calcFieldBombs(self):
        """Calculate bombs for each point on the field."""
        for point in self:
            if self[point] == Value.bomb or self[point] == Value.barrier:
                continue
            bombsAround = 0
            # for bias in Point.range(-1, 2):
            for bias in self.pattern(point):
                if bias != (0, 0):
                    bombsAround += self[point + bias] == Value.bomb
            self[point] = Value(bombsAround)

    def __iter__(self):
        """Iterate over all cordinates of the field."""
        yield from Point.range([self.width, self.height])

    def toggleFlag(self, x, y=None):
        """Toggle sure flag."""
        x, y = Point(x, y)
        self[x, y] = Flag.sure if self[x, y] == Flag.noflag else Flag.noflag

    def cycleFlag(self, x, y=None):
        """Change flag value on a point."""
        x, y = Point(x, y)
        if self[x, y] == Flag.noflag:
            self[x, y] = Flag.sure
        elif self[x, y] == Flag.sure:
            self[x, y] = Flag.guess
        elif self[x, y] == Flag.guess:
            self[x, y] = Flag.noflag

    def reveal(self, x, y=None):
        """
        Reveal all possible minepoints around coordinate.

        Return freshly revealed list of coordinates or None if Bomb was opened
        """
        point = Point(x, y)
        if self[point] == Value.bomb:
            return None
        if self[point] == Mask.opened:
            return []

        revealed = []
        stack = [point]

        while len(stack):
            point = stack.pop()
            self[point] = Mask.opened
            revealed.append(point)

            for bias in self.pattern(point):
                curPos = point + bias
                if self[curPos] != Mask.closed or self[curPos] != Flag.noflag:
                    continue

                if self[curPos] == Value.empty:
                    self[curPos] = Mask.pending
                    stack.append(curPos)
                elif self[curPos] != Value.bomb and self[curPos] != Value.barrier:
                    self[curPos] = Mask.opened
                    revealed.append(curPos)
        return revealed

    def statistic(self):
        """Return current field statistic."""
        res = {
            'cellsOpened': 0,
            'bombsMarked': 0,
            'bombsGuessed': 0,
            'cellsRemaning': 0,
            'cellsTotal': 0,
            'bombsLeft': 0,
            'allBombsCorrect': True
        }
        for x, y in self:
            cell = self[x, y]
            if cell == Mask.opened:
                res['cellsOpened'] += 1
            else:
                if cell == Flag.sure:
                    res['bombsMarked'] += 1
                if cell == Value.bomb and cell == Flag.sure:
                    res['bombsGuessed'] += 1
        res['cellsTotal'] = res['cellsOpened'] + res['bombsMarked']
        res['cellsRemaning'] = self.size - res['cellsOpened'] - res['bombsGuessed']
        res['bombsLeft'] = self.bombs - res['bombsMarked']
        res['allBombsCorrect'] = res['bombsGuessed'] == self.bombs
        return res

    def recalculate(self):
        """Recalculate field values after manual changes."""
        self.__calcFieldBombs()

    def dump(self):
        """Dump field data to console."""
        for y in range(self.height):
            for x in range(self.width):
                print(f'{str(self[x, y]):>2}', end=' ')
            print()
        print()
