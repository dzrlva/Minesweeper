"""Hexagon distance tests."""

import unittest
from unittest.mock import MagicMock

from gui import hexagon

class TestMock(unittest.TestCase):
    """Test class for hexagon."""

    def test1(self):
        """Distance on x and y with centered hexagon."""
        center_hex = hexagon.Hexagon(None, 0, 0, 0.0, None, None, None)
        self.f = MagicMock(return_value=2.0)
        self.assertEqual(self.f(), center_hex.distance(2**(1/2)))
        self.assertEqual(self.f(), center_hex.distance(-2**(1/2)))
        self.assertEqual(self.f(), center_hex.distance(x=2**(1/2), y=-2**(1/2)))
        self.assertEqual(self.f(), center_hex.distance(x=-2**(1/2), y=2**(1/2)))

    def test2(self):
        """Distance on x with centered hexagon."""
        center_hex = hexagon.Hexagon(None, 0, 0, 0.0, None, None, None)
        self.f = MagicMock(return_value=5.0)
        self.assertEqual(self.f(), center_hex.distance(x=5.0, y=0.0))
        self.assertEqual(self.f(), center_hex.distance(x=-5.0, y=0.0))

    def test3(self):
        """Distance on y with centered hexagon."""
        center_hex = hexagon.Hexagon(None, 0, 0, 0.0, None, None, None)
        self.f = MagicMock(return_value=7.0)
        self.assertEqual(self.f(), center_hex.distance(x=0.0, y=7.0))
        self.assertEqual(self.f(), center_hex.distance(x=0.0, y=-7.0))

    def test4(self):
        """Distance between center and hexagon."""
        center_hex = hexagon.Hexagon(None, 0, 0, 0.0, None, None, None)
        self.f = MagicMock(return_value=0.0)
        self.assertEqual(self.f(), center_hex.distance(0.0))

    def test5(self):
        """Distance on x and y with positive hexagon."""
        pos_hex = hexagon.Hexagon(None, 3, 4, 0.0, None, None, None)
        self.f = MagicMock(return_value=5.0)
        self.g = MagicMock(return_value=13.0)

        self.assertEqual(self.f(), pos_hex.distance(0))
        self.assertEqual(self.f(), pos_hex.distance(6, 8))
        self.assertEqual(self.f(), pos_hex.distance(0, 8))
        self.assertEqual(self.f(), pos_hex.distance(6, 0))

        self.assertEqual(self.f(), pos_hex.distance(-1, 1))
        self.assertEqual(self.f(), pos_hex.distance(-1, 7))
        self.assertEqual(self.f(), pos_hex.distance(7, 1))
        self.assertEqual(self.f(), pos_hex.distance(7, 7))

        self.assertEqual(self.g(), pos_hex.distance(-2, 16))
        self.assertEqual(self.g(), pos_hex.distance(-2, -8))
        self.assertEqual(self.g(), pos_hex.distance(8, 16))
        self.assertEqual(self.g(), pos_hex.distance(8, -8))

        self.assertEqual(self.g(), pos_hex.distance(15, -1))
        self.assertEqual(self.g(), pos_hex.distance(15, 9))
        self.assertEqual(self.g(), pos_hex.distance(-9, -1))
        self.assertEqual(self.g(), pos_hex.distance(-9, 9))

    def test6(self):
        """Distance on x with positive hexagon."""
        pos_hex = hexagon.Hexagon(None, 3, 4, 0.0, None, None, None)
        self.f = MagicMock(return_value=5.0)
        self.assertEqual(self.f(), pos_hex.distance(x=8, y=4))
        self.assertEqual(self.f(), pos_hex.distance(x=-2, y=4))

    def test7(self):
        """Distance on y with positive hexagon."""
        pos_hex = hexagon.Hexagon(None, 3, 4, 0.0, None, None, None)
        self.f = MagicMock(return_value=5.0)
        self.assertEqual(self.f(), pos_hex.distance(x=3, y=9))
        self.assertEqual(self.f(), pos_hex.distance(x=3, y=-1))

    def test8(self):
        """Distance between center and positive hexagon."""
        pos_hex = hexagon.Hexagon(None, 3, 4, 0.0, None, None, None)
        self.f = MagicMock(return_value=0.0)
        self.assertEqual(self.f(), pos_hex.distance(3, 4))

    def test9(self):
        """Distance on x and y with negative hexagon."""
        pos_hex = hexagon.Hexagon(None, -7, -16, 0.0, None, None, None)
        self.f = MagicMock(return_value=17.0)

        self.assertEqual(self.f(), pos_hex.distance(1, -1))
        self.assertEqual(self.f(), pos_hex.distance(1, -31))
        self.assertEqual(self.f(), pos_hex.distance(-15, -1))
        self.assertEqual(self.f(), pos_hex.distance(-15, -31))

        self.assertEqual(self.f(), pos_hex.distance(8, -8))
        self.assertEqual(self.f(), pos_hex.distance(8, -24))
        self.assertEqual(self.f(), pos_hex.distance(-22, -8))
        self.assertEqual(self.f(), pos_hex.distance(-22, -24))

    def test10(self):
        """Distance on x with negative hexagon."""
        pos_hex = hexagon.Hexagon(None, -7, -16, 0.0, None, None, None)
        self.f = MagicMock(return_value=10.0)
        self.assertEqual(self.f(), pos_hex.distance(-17, -16))
        self.assertEqual(self.f(), pos_hex.distance(3, -16))

    def test11(self):
        """Distance on y with negative hexagon."""
        pos_hex = hexagon.Hexagon(None, -7, -16, 0.0, None, None, None)
        self.f = MagicMock(return_value=20.0)
        self.assertEqual(self.f(), pos_hex.distance(-7, 4))
        self.assertEqual(self.f(), pos_hex.distance(-7, -36))

    def test12(self):
        """Distance between center and negative hexagon."""
        pos_hex = hexagon.Hexagon(None, -7, -16, 0.0, None, None, None)
        self.f = MagicMock(return_value=0.0)
        self.assertEqual(self.f(), pos_hex.distance(-7, -16))

if __name__ == "__main__":
    unittest.main()