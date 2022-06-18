"""Coordinate range tests."""

import unittest
from unittest.mock import MagicMock

#import sys
#sys.path.append('../util')
#from coord import Coord


from minesweeper.util import coord


class TestMock(unittest.TestCase):
    """Coordinate tests of range method."""

    def test1(self):
        """Range with no input begin value."""
        val = 3
        self.f = MagicMock(return_value=list(coord.Coord(i, j) for i in range(val) for j in range(val)))
        a = coord.Coord(val, val)
        self.assertEqual(self.f(), list(coord.Coord.range(a)))

    def test2(self):
        """Range with same values for x and y."""
        val = 5
        self.f = MagicMock(return_value=list(coord.Coord(i, j) for i in range(val) for j in range(val)))
        a = coord.Coord(0, 0)
        b = coord.Coord(val, val)
        self.assertEqual(self.f(), list(coord.Coord.range(a, b)))

    def test3(self):
        """Range with different values for x and y."""
        val = 5
        self.f = MagicMock(return_value=list(coord.Coord(i, j) for i in range(val) for j in range(2*val)))
        a = coord.Coord(0, 0)
        b = coord.Coord(val, 2*val)
        self.assertEqual(self.f(), list(coord.Coord.range(a, b)))

    def test4(self):
        """Range with given step."""
        val = 5
        self.f = MagicMock(return_value=list(coord.Coord(i, j) for i in range(val) for j in range(0, 2*val, 2)))
        a = coord.Coord(0, 0)
        b = coord.Coord(val, 2*val)
        c = coord.Coord(1, 2)
        self.assertEqual(self.f(), list(coord.Coord.range(a, b, c)))

    def test5(self):
        """Range with too big step."""
        val = 5
        a = coord.Coord(0, 0)
        self.f = MagicMock(return_value=[a])
        b = coord.Coord(val, val)
        c = coord.Coord(2*val, 2*val)
        self.assertEqual(self.f(), list(coord.Coord.range(a, b, c)))

    def test6(self):
        """Incorrect range borders for x."""
        a = coord.Coord(4, 2)
        b = coord.Coord(2, 4)
        with self.assertRaises(ValueError):
            self.f = MagicMock(return_value=list(coord.Coord.range(a, b)))

    def test7(self):
        """Incorrect range borders for y."""
        a = coord.Coord(2, 4)
        b = coord.Coord(4, 2)
        with self.assertRaises(ValueError):
            self.f = MagicMock(return_value=list(coord.Coord.range(a, b)))

if __name__ == "__main__":
    unittest.main()
