import unittest
from WishNum import finding


class TestMath(unittest.TestCase):
    def test_1(self):
        self.assertEqual(finding(2, 0, 6), (2, 3))

    def test_2(self):
        self.assertEqual(finding(2,2,10), (2, 3))

    def test_3(self):
        self.assertEqual(finding(100, 0, 6), (100, None))

    def test_4(self):
        self.assertEqual(finding(-100, 0, 6), (-100, None))

    def test_5(self):
        self.assertEqual(finding(-4, -5, -1), (-4, 3))

    def test_6(self):
        self.assertEqual(finding(100, -10, 500), (100, 9))

    def test_7(self):
        self.assertEqual(finding(1, -100, 100), (1, 7))

    def test_8(self):
        self.assertEqual(finding(37, 1, 59), (37, 3))

    def test_9(self):
        self.assertEqual(finding(100, 1, 100), (100, 7))

    def test_10(self):
        self.assertEqual(finding(105, -123, 637), (105, 9))