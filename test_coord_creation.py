"""Coordinate creation tests."""

import unittest
from unittest.mock import MagicMock

#import sys
#sys.path.append('../util')
#from coord import Coord


from util import coord


class TestMock(unittest.TestCase):
    """Coordinate __init__ tests."""

    def test1(self):
        """Creation from int."""
        self.f = MagicMock(return_value=coord.Coord(2, 2))
        val = coord.Coord(coord.Coord(2))
        self.assertEqual(self.f(), val)

    def test2(self):
        """Creation from Cord."""
        self.f = MagicMock(return_value=coord.Coord(2, 2))
        val = coord.Coord(coord.Coord(2,2))
        self.assertEqual(self.f(), val)

    def test3(self):
        """Creation from floats."""
        self.f = MagicMock(return_value=coord.Coord(1, 3))
        val = coord.Coord(coord.Coord(1.25, 3.8))
        self.assertEqual(self.f(), val)

    def test4(self):
        """Creation from int and float."""
        self.f = MagicMock(return_value=coord.Coord(1, 3))
        val = coord.Coord(coord.Coord(1, 3.8))
        self.assertEqual(self.f(), val)

    def test5(self):
        """Creation from int tuple."""
        self.f = MagicMock(return_value=coord.Coord(1, 3))
        val = coord.Coord(coord.Coord((1, 3)))
        self.assertEqual(self.f(), val)

    def test6(self):
        """Creation from float tuple."""
        self.f = MagicMock(return_value=coord.Coord(1, 3))
        val = coord.Coord(coord.Coord((1.59, 3.113)))
        self.assertEqual(self.f(), val)

    def test7(self):
        """Creation from float list."""
        self.f = MagicMock(return_value=coord.Coord(1, 3))
        val = coord.Coord(coord.Coord([1.59, 3.113]))
        self.assertEqual(self.f(), val)

    def test8(self):
        """Creation from dictionary with 'x' and 'y'."""
        self.f = MagicMock(return_value=coord.Coord(1, 3))
        val = coord.Coord(coord.Coord({'x': 1.5, 'y': 3.1}))
        self.assertEqual(self.f(), val)

    def test9(self):
        """Creation from dictionary with additional keys."""
        self.f = MagicMock(return_value=coord.Coord(1, 3))
        val = coord.Coord(coord.Coord({'x': 1, 'y': 3, 'z': 100500, 'no_use': 50}))
        self.assertEqual(self.f(), val)

    def test10(self):
        """Incorrect list length."""
        with self.assertRaises(ValueError):
            self.f = MagicMock(return_value=coord.Coord([1, 2, 3]))

    def test11(self):
        """Incorrect dictionary."""
        with self.assertRaises(ValueError):
            self.f = MagicMock(return_value=coord.Coord({'x': 4}))

    def test12(self):
        """Incorrect amount of arguments."""
        with self.assertRaises(TypeError):
            self.f = MagicMock(return_value=coord.Coord(1, 2, 10))

if __name__ == "__main__":
    unittest.main()