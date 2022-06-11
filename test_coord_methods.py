"""Coordinate methods tests."""

import unittest
from unittest.mock import MagicMock

#import sys
#sys.path.append('../util')
#from coord import Coord


from util import coord


class TestMock(unittest.TestCase):
    """Coordinate tests of methods."""

    def test1(self):
        """Coords __getitem__ method."""
        self.f = MagicMock(return_value=5)
        self.g = MagicMock(return_value=10)
        val = coord.Coord(coord.Coord(5, 10))
        self.assertEqual(self.f(), val[0])
        self.assertEqual(self.f(), val['x'])
        self.assertEqual(self.g(), val[1])
        self.assertEqual(self.g(), val['y'])

    def test2(self):
        """Coords __setitem__ method."""
        self.f = MagicMock(return_value=7)
        self.g = MagicMock(return_value=19)
        val = coord.Coord(coord.Coord(5, 10))
        val[0] = 7
        val['y'] = 19
        self.assertEqual(self.f(), val['x'])
        self.assertEqual(self.g(), val[1])

    def test3(self):
        """Coords string conversion."""
        self.f = MagicMock(return_value="(5, 7)")
        self.assertEqual(self.f(), str(coord.Coord(5, 7)))

    def test4(self):
        """Coords text conversion."""
        self.f = MagicMock(return_value="Coord <5, 7>")
        self.assertEqual(self.f(), repr(coord.Coord(5, 7)))

if __name__ == "__main__":
    unittest.main()