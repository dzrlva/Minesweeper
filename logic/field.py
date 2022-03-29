#!/usr/bin/env python

"""Module for the Field class."""

from coord import Coord
from minepoint import MinePoint, Value, Mask, Flag


class Field:
    """Logic for minesweeper minefield."""

    OUTOFBOUND = -1

    def __init__(self, size, bombsPercent):
        """Initialize field with size and bombs. Randomly fill it."""
        self.size = size
        self.bombs = round(size * size * bombsPercent)
        self.__field = [[MinePoint() for _ in range(size)]
                        for _ in range(size)]
        self.__randomizeBombs()
        self.__calcFieldBombs()

    def __isOutOfBounds(self, x, y=None):
        x, y = Coord(x, y)
        return x < 0 or y < 0 or x >= self.size or y >= self.size

    def __getitem__(self, coords):
        """Return field minepoint if in bound else OUTOFBOUND value."""
        x, y = Coord(coords)
        if self.__isOutOfBounds(x, y):
            return Field.OUTOFBOUND
        return self.__field[x][y]

    def __setitem__(self, coords, value):
        """Set minepoint value if in bound."""
        x, y = Coord(coords)
        if self.__isOutOfBounds(x, y):
            raise ValueError(f'Coords {coords} are out of bounds')
        self.__field[x][y].set(value)

    def __randomizeBombs(self):
        """Randomize bomb position."""
        for _ in range(self.bombs):
            x, y = Coord.random(self.size)
            while self[x, y] == Value.bomb:
                x, y = Coord.random(self.size)
            self[x, y] = Value.bomb

    def __calcFieldBombs(self):
        """Calculate bombs for each point on the field."""
        for point in Coord.range(self.size):
            if self[point] == Value.bomb:
                continue
            bombsAround = 0
            for bias in Coord.range(-1, 2):
                if bias != (0, 0):
                    bombsAround += self[point + bias] == Value.bomb
            self[point] = Value(bombsAround)

    def __iter__(self):
        """Iterate over all cordinates of the field."""
        yield from Coord.range(self.size)

    def cycleFlag(self, x, y=None):
        """Change flag value on a point."""
        x, y = Coord(x, y)
        if self[x, y] == Flag.noflag:
            self[x, y] = Flag.sure
        elif self[x, y] == Flag.sure:
            self[x, y] = Flag.guess
        elif self[x, y] == Flag.guess:
            self[x, y] = Flag.noflag

    def reveal(self, x, y=None):
        """
        Reveal all possible minepoints around coordinate
        Return True if revealed point has a bomb
        """
        point = Coord(x, y)
        if self[point] == Value.bomb:
            return True
        if self[point] == Mask.opened:
            return False

        stack = [point]
        while len(stack):
            point = stack.pop()
            self[point] = Mask.opened

            for bias in Coord.range(-1, 2):
                curPos = point + bias
                if self[curPos] != Mask.closed:
                    continue

                if self[curPos] == Value.empty:
                    self[curPos] = Mask.pending
                    stack.append(curPos)
                elif self[curPos] != Value.bomb:
                    self[curPos] = Mask.opened
        return False
