import requests
import logging
import unittest
import io

class TestGetCurrencies(unittest.TestCase):

    def test_correct_currencies(self):
        try:
            result = get_currencies(["USD", "EUR"])
            self.assertIn("USD", result)
            self.assertIn("EUR", result)
            self.assertIsInstance(result["USD"], float)
            self.assertIsInstance(result["EUR"], float)
            self.assertGreater(result["USD"], 0)
            self.assertGreater(result["EUR"], 0)
        except ConnectionError:
            self.skipTest("API недоступен")

    def test_nonexistent_currency(self):
        with self.assertRaises(KeyError) as context:
            get_currencies(["NONEXISTENT_CURRENCY"])
        self.assertIn("NONEXISTENT_CURRENCY", str(context.exception))

    def test_connection_error(self):
        with self.assertRaises(ConnectionError):
            get_currencies(["USD"], url="https://")


class TestLoggerDecorator(unittest.TestCase):

    def setUp(self):
        self.stream = io.StringIO()

    def test_logging_success_start_message(self):

        @logger(handle=self.stream)
        def test_function(x):
            return x * 2

        result = test_function(5)

        logs = self.stream.getvalue()
        self.assertIn("INFO", logs)
        self.assertIn("Вызов test_function", logs)
        self.assertIn("args = (5,)", logs)
        self.assertEqual(result, 10)

    def test_logging_success_end_message(self):

        @logger(handle=self.stream)
        def test_function(x):
            return x * 2

        result = test_function(5)

        logs = self.stream.getvalue()
        self.assertIn("INFO", logs)
        self.assertIn("вернула 10", logs)

    def test_logging_arguments(self):

        @logger(handle=self.stream)
        def test_function(a, b, c=10):
            return a + b + c

        result = test_function(1, 2, c=3)

        logs = self.stream.getvalue()
        self.assertIn("args = (1, 2)", logs)
        self.assertIn("c", logs)
        self.assertEqual(result, 6)

    def test_logging_return_value(self):

        @logger(handle=self.stream)
        def test_function():
            return {"key": "value"}

        result = test_function()

        logs = self.stream.getvalue()
        self.assertIn("key", logs)
        self.assertIn("value", logs)
        self.assertEqual(result, {"key": "value"})

    def test_logging_error(self):

        @logger(handle=self.stream)
        def error_function():
            raise ValueError("Test error")

        with self.assertRaises(ValueError):
            error_function()

        logs = self.stream.getvalue()
        self.assertRegex(logs, r"ERROR")
        self.assertIn("ValueError", logs)
        self.assertIn("Test error", logs)

    def test_exception_propagation(self):

        @logger(handle=self.stream)
        def error_function():
            raise RuntimeError("Propagated error")

        with self.assertRaises(RuntimeError) as context:
            error_function()

        self.assertEqual(str(context.exception), "Propagated error")

    def test_decorator_without_parentheses(self):

        @logger
        def simple_function(x):
            return x**2

        result = simple_function(4)
        self.assertEqual(result, 16)

    def test_decorator_with_logging_logger(self):
        test_logger = logging.getLogger("test_logger")
        test_logger.setLevel(logging.DEBUG)

        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        handler.setLevel(logging.DEBUG)
        test_logger.addHandler(handler)

        @logger(handle=test_logger)
        def logged_function(x):
            return x + 1

        result = logged_function(10)

        logs = log_stream.getvalue()
        self.assertIn("Вызов logged_function", logs)
        self.assertIn("вернула 11", logs)
        self.assertEqual(result, 11)


class TestStreamWrite(unittest.TestCase):


    def setUp(self):
        self.stream = io.StringIO()

        @logger(handle=self.stream)
        def wrapped():
            try:
                response = requests.get("https://invalid-url-12345.invalid")
                response.raise_for_status()
                data = response.json()
            except requests.exceptions.RequestException as e:
                raise ConnectionError(f"API недоступен: {e}") from e
            return data

        self.wrapped = wrapped

    def test_logging_error(self):
        with self.assertRaises(ConnectionError):
            self.wrapped()

        logs = self.stream.getvalue()
        self.assertIn("ERROR", logs)
        self.assertIn("ConnectionError", logs)


class TestSolveQuadratic(unittest.TestCase):

    def test_two_roots(self):
        roots = solve_quadratic(1, -5, 6)
        self.assertIsNotNone(roots)
        self.assertEqual(len(roots), 2)
        self.assertIn(2.0, roots)
        self.assertIn(3.0, roots)

    def test_one_root(self):
        roots = solve_quadratic(1, -2, 1)
        self.assertIsNotNone(roots)
        self.assertEqual(len(roots), 1)
        self.assertEqual(roots[0], 1.0)

    def test_no_real_roots(self):
        roots = solve_quadratic(1, 0, 1)
        self.assertIsNone(roots)

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            solve_quadratic("abc", 1, 1)

    def test_critical_both_zero(self):
        roots = solve_quadratic(0, 0, 5)
        self.assertIsNone(roots)

    def test_linear_equation(self):
        roots = solve_quadratic(0, 2, -4)
        self.assertIsNotNone(roots)
        self.assertEqual(len(roots), 1)
        self.assertEqual(roots[0], 2.0)