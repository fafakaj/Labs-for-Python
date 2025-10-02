import unittest
from binary_tree import dict_bin_tree, custom_left, custom_right

class TestMath(unittest.TestCase):
    def test_1(self):
        self.assertEqual(dict_bin_tree(1), {0: 10})
    def test_2(self):
        self.assertEqual(dict_bin_tree(2), {0: 10, 1: 31, 2: 29})
    def test_3(self):
        self.assertEqual(dict_bin_tree(3), {0: 10, 1: 31, 2: 29, 3: 94, 4: 92, 5: 88, 6: 86})
    def test_4(self):
        self.assertEqual(dict_bin_tree(5), {0: 10, 1: 31, 2: 29, 3: 94, 4: 92, 5: 88, 6: 86, 7: 283,
        8: 281, 9: 277, 10: 275, 11: 265, 12: 263, 13: 259, 14: 257, 15: 850, 16: 848, 17: 844, 18: 842,
        19: 832, 20: 830, 21: 826, 22: 824, 23: 796, 24: 794, 25: 790, 26: 788, 27: 778, 28: 776, 29: 772, 30: 770})
    def test_5(self):
        self.assertEqual(dict_bin_tree(3, l_b=custom_left, r_b=custom_right), {0: 10, 1: 11, 2: 9, 3: 12, 4: 10, 5: 10, 6: 8})