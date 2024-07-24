import unittest
import math

import core


class TestShape(unittest.TestCase):

    def test_circle(self):
        self.assertEqual(core.circle(4), 16*math.pi)

    def test_triangle(self):
        self.assertEqual(core.triangle(3, 4, 5), 6)

    def test_right_triangle_true(self):
        self.assertTrue(core.right_triangle(3, 4, 5))

    def test_right_triangle_false(self):
        self.assertFalse(core.right_triangle(3, 3, 3))


if __name__ == "__main__":
    unittest.main()
