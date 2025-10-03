import unittest
from binary_tree import dict_bin_tree


def custom_left(x: int) -> int:
    return x + 1
# Пользовательская функция для значения левого корня

def custom_right(x: int) -> int:
    return x - 1
# Пользовательская функция для значения правого корня


class TestMath(unittest.TestCase):
    def test_1(self):
        self.assertEqual(dict_bin_tree(2, 111), {0: 111, 1: 334, 2: 332})
    def test_2(self):
        self.assertEqual(dict_bin_tree(3), {0: 10, 1: 31, 2: 29, 3: 94, 4: 92, 5: 88, 6: 86})
    def test_3(self):
        self.assertEqual(dict_bin_tree(5), {0: 10, 1: 31, 2: 29, 3: 94, 4: 92, 5: 88, 6: 86, 7: 283,
        8: 281, 9: 277, 10: 275, 11: 265, 12: 263, 13: 259, 14: 257, 15: 850, 16: 848, 17: 844, 18: 842,
        19: 832, 20: 830, 21: 826, 22: 824, 23: 796, 24: 794, 25: 790, 26: 788, 27: 778, 28: 776, 29: 772, 30: 770})
    def test_4(self):
        self.assertEqual(dict_bin_tree(3, l_b = custom_left, r_b = custom_right),
                         {0: 10, 1: 11, 2: 9, 3: 12, 4: 10, 5: 10, 6: 8})
    def test_5(self):
        self.assertEqual(dict_bin_tree(3, 55, l_b = custom_left),
                         {0: 55, 1: 56, 2: 164, 3: 57, 4: 167, 5: 165, 6: 491})
    def test_6(self):
        self.assertEqual(dict_bin_tree(2, 111, r_b = custom_right),
                         {0: 111, 1: 334, 2: 110})
    def test_7(self):
        self.assertEqual(dict_bin_tree(3, 15, l_b = custom_left, r_b = custom_right),
                         {0: 15, 1: 16, 2: 14, 3: 17, 4: 15, 5: 15, 6: 13})