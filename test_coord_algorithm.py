"""Coordinate arithmetic tests."""

import unittest
from unittest.mock import MagicMock

#import sys
#sys.path.append('../util')
#from coord import Coord


from util import coord


class TestMock(unittest.TestCase):
    """Coordinate tests of arithmetic operations."""

    def test1(self):
        """Positive coord + positive coord."""
        self.f = MagicMock(return_value=coord.Coord(15, 10))
        self.assertEqual(self.f(), coord.Coord(5, 3) + coord.Coord(10, 7))

    def test2(self):
        """Positive coord + negative coord."""
        self.f = MagicMock(return_value=coord.Coord(2, 1))
        self.assertEqual(self.f(), coord.Coord(5, 3) + coord.Coord(-3, -2))

    def test3(self):
        """Positive coord + pos/neg coord."""
        self.f = MagicMock(return_value=coord.Coord(1, 9))
        self.assertEqual(self.f(), coord.Coord(5, 3) + coord.Coord(-4, 6))

    def test4(self):
        """Negative coord."""
        self.f = MagicMock(return_value=coord.Coord(-1, -2))
        self.assertEqual(self.f(), -coord.Coord(1,2))

    def test5(self):
        """Coords subtraction, result with coords > 0."""
        self.f = MagicMock(return_value=coord.Coord(1, 3))
        self.assertEqual(self.f(), coord.Coord(10, 7)-coord.Coord(9, 4))

    def test6(self):
        """Coords subtraction, result with coords < 0."""
        self.f = MagicMock(return_value=coord.Coord(-1, -3))
        self.assertEqual(self.f(), coord.Coord(9, 4)-coord.Coord(10, 7))

    def test7(self):
        """Negative coord subtraction."""
        self.f = MagicMock(return_value=coord.Coord(5, 7))
        self.assertEqual(self.f(), coord.Coord(1, 4) - coord.Coord(-4, -3))

    def test8(self):
        """Coord division."""
        self.f = MagicMock(return_value=coord.Coord(2, 4))
        a = coord.Coord(12, 12)
        b = coord.Coord(5, 3)
        self.assertEqual(self.f(), a/b)
        self.assertEqual(self.f(), a//b)

    def test9(self):
        """Coord equal comparison."""
        self.f = MagicMock(return_value=True)
        self.g = MagicMock(return_value=False)
        self.assertEqual(self.f(), coord.Coord(5, 3) == coord.Coord([5, 3]))
        self.assertEqual(self.f(), coord.Coord(7, 7) == 7)
        self.assertEqual(self.g(), coord.Coord(3, 5) == coord.Coord([5, 3]))
        self.assertEqual(self.g(), coord.Coord(3, 10) == coord.Coord({'x': 3, 'y': 100, 'z': 10}))

    def test10(self):
        """Coord inversion."""
        self.f = MagicMock(return_value=coord.Coord(7, 5))
        self.assertEqual(self.f(), ~coord.Coord(5, 7))

    def test11(self):
        """Coord operator combination."""
        self.f = MagicMock(return_value=coord.Coord(1, 2))
        a = coord.Coord(5, 7)
        b = coord.Coord(6, 9)
        c = coord.Coord(4, -6)
        d = coord.Coord(10, 1)
        self.assertEqual(self.f(), -((b - ~a) + c//d))

    def test12(self):
        """Coord zero division."""
        with self.assertRaises(ZeroDivisionError):
            self.f = MagicMock(return_value=coord.Coord(5, 10)//coord.Coord(5, 0))

if __name__ == "__main__":
    unittest.main()