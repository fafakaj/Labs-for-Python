import unittest
from models.currency import Currency


class TestCurrency(unittest.TestCase):
    def test_currency_creation(self):
        currency = Currency("840", "USD", "Доллар США", 90.5, 1)
        self.assertEqual(currency.char_code, "USD")
        self.assertEqual(currency.value, 90.5)
        self.assertEqual(currency.nominal, 1)

    def test_currency_validation(self):
        currency = Currency("840", "USD", "Доллар США", 90.5, 1)

        with self.assertRaises(ValueError):
            currency.value = -10

        with self.assertRaises(ValueError):
            currency.char_code = "AB"


if __name__ == '__main__':
    unittest.main()