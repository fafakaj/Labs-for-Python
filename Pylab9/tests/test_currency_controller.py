import unittest
from unittest.mock import MagicMock
from controllers.currencycontroller import CurrencyController
from models.currency import Currency


class TestCurrencyController(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.controller = CurrencyController(self.mock_db)

    def test_list_currencies(self):
        self.mock_db._read_currencies.return_value = [
            {"id": 1, "char_code": "USD", "value": 90.5, "name": "Доллар США"}
        ]
        result = self.controller.list_currencies()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['char_code'], "USD")
        self.mock_db._read_currencies.assert_called_once()

    def test_create_currency(self):
        self.mock_db._create_currency.return_value = 1
        currency = self.controller.create_currency("840", "USD", "Доллар США", 90.5, 1)
        self.assertIsInstance(currency, Currency)
        self.assertEqual(currency.char_code, "USD")
        self.mock_db._create_currency.assert_called_once()

    def test_delete_currency(self):
        self.mock_db._delete_currency.return_value = True
        result = self.controller.delete_currency(1)
        self.assertTrue(result)
        self.mock_db._delete_currency.assert_called_once_with(1)


if __name__ == '__main__':
    unittest.main()