import unittest
from codeforlab3 import binary_tree


def custom_left(x: int) -> int:
    return x + 1
# Пользовательская функция для левого корня

def custom_right(x: int) -> int:
    return x - 1
# Пользовательская функция для правого корня


class TestMath(unittest.TestCase):
    def test_1(self):
        self.assertEqual(binary_tree(2, 111), {'111': [{'334': []}, {'332': []}]})

    def test_2(self):
        self.assertEqual(binary_tree(3),
                         {'10': [{'31': [{'94': []}, {'92': []}]}, {'29': [{'88': []}, {'86': []}]}]})

    def test_3(self):
        self.assertEqual(binary_tree(5),
                         {'10': [{'31': [{'94': [{'283': [{'850': []}, {'848': []}]}, {'281': [{'844': []}, {'842': []}]}]},
                                {'92': [{'277': [{'832': []}, {'830': []}]}, {'275': [{'826': []},
                                {'824': []}]}]}]}, {'29': [{'88': [{'265': [{'796': []}, {'794': []}]},
                                {'263': [{'790': []}, {'788': []}]}]}, {'86': [{'259': [{'778': []},
                                {'776': []}]}, {'257': [{'772': []}, {'770': []}]}]}]}]})

    def test_4(self):
        self.assertEqual(binary_tree(3, l_b=custom_left, r_b=custom_right),
                         {'10': [{'11': [{'12': []}, {'10': []}]}, {'9': [{'10': []}, {'8': []}]}]})

    def test_5(self):
        self.assertEqual(binary_tree(3, 55, l_b=custom_left),
                         {'55': [{'56': [{'57': []}, {'167': []}]}, {'164': [{'165': []}, {'491': []}]}]})

    def test_6(self):
        self.assertEqual(binary_tree(2, 111, r_b=custom_right),
                         {'111': [{'334': []}, {'110': []}]})

    def test_7(self):
        self.assertEqual(binary_tree(3, 15, l_b=custom_left, r_b=custom_right),
                         {'15': [{'16': [{'17': []}, {'15': []}]}, {'14': [{'15': []}, {'13': []}]}]})