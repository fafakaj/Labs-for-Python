import requests
import sys
import functools
import logging
import math
import unittest
import io


def logger(func=None, *, handle=sys.stdout):
    def decorator(f):
        @functools.wraps(f)
        def inner(*args, **kwargs):
            is_logger = hasattr(handle, "info") and callable(getattr(handle, "info"))
            if is_logger:
                handle.info(
                    f"[INFO] Вызов {f.__name__} c args = {args}, kwargs = {kwargs}"
                )
                try:
                    result = f(*args, **kwargs)
                    handle.info(f"[INFO] {f.__name__} вернула {result}")
                    return result
                except Exception as e:
                    handle.error(
                        f"[ERROR] {f.__name__} выбросила {type(e).__name__}: {e}"
                    )
                    raise
            else:
                handle.write(
                    f"[INFO] Вызов {f.__name__} c args = {args}, kwargs = {kwargs}\n"
                )
                try:
                    result = f(*args, **kwargs)
                    handle.write(f"[INFO] {f.__name__} вернула {result}\n")
                    return result
                except Exception as e:
                    handle.write(
                        f"[ERROR] {f.__name__} выбросила {type(e).__name__}: {e}\n"
                    )
                    raise

        return inner

    if func is None:
        return decorator
    else:
        return decorator(func)


@logger()
def get_currencies(currency_codes: list, url: str = "https://www.cbr-xml-daily.ru/daily_json.js") -> dict:
    """
    Получает курсы валют с API Центробанка России.

    Args:
        currency_codes (list): Список символьных кодов валют (например, ['USD', 'EUR']).

    Returns:
        dict: Словарь, где ключи - символьные коды валют, а значения - их курсы.
              Возвращает None в случае ошибки запроса.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"API недоступен: {e}") from e
    except ValueError as e:
        raise ValueError("Некорректный JSON") from e

    if "Valute" not in data:
        raise KeyError("Ответ не содержит ключ 'Valute'")

    result = {}
    for code in currency_codes:
        if code not in data["Valute"]:
            raise KeyError(f"Валюта '{code}' отсутствует в данных")

        value = data["Valute"][code].get("Value")
        if not isinstance(value, (int, float)):
            raise TypeError(f"Курс валюты '{code}' имеет неверный тип: {type(value)}")

        result[code] = float(value)

    return result


file_logger = logging.getLogger("currency_file")
file_logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("../currency.log", mode="a", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

if not file_logger.handlers:
    file_logger.addHandler(file_handler)

@logger(handle=file_logger)
def get_currencies_file_logged(currency_codes: list, url: str = "https://www.cbr-xml-daily.ru/daily_json.js") -> dict:
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"API недоступен: {e}") from e
    except ValueError as e:
        raise ValueError("Некорректный JSON") from e

    if "Valute" not in data:
        raise KeyError("Ответ не содержит ключ 'Valute'")

    result = {}
    for code in currency_codes:
        if code not in data["Valute"]:
            raise KeyError(f"Валюта '{code}' отсутствует в данных")

        value = data["Valute"][code].get("Value")
        if not isinstance(value, (int, float)):
            raise TypeError(f"Курс валюты '{code}' имеет неверный тип: {type(value)}")

        result[code] = float(value)

    return result

quadratic_logger = logging.getLogger("quadratic")
quadratic_logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)

if not quadratic_logger.handlers:
    quadratic_logger.addHandler(console_handler)


def logger_for_demo(func=None, *, handle=sys.stdout):
    def decorator(f):
        @functools.wraps(f)
        def inner(*args, **kwargs):
            is_logger = hasattr(handle, "info") and callable(getattr(handle, "info"))

            if is_logger:
                handle.info(f"Вызов {f.__name__} c args = {args}, kwargs = {kwargs}")
                try:
                    result = f(*args, **kwargs)
                    if isinstance(result, tuple) and len(result) == 3:
                        status, msg, roots = result
                        if status == "INFO":
                            handle.info(f"{f.__name__}: {msg}, корни: {roots}")
                        elif status == "WARNING":
                            handle.warning(f"{f.__name__}: {msg}")
                        elif status == "CRITICAL":
                            handle.critical(f"{f.__name__}: {msg}")
                        return roots
                    else:
                        handle.info(f"{f.__name__} вернула {result}")
                    return result
                except Exception as e:
                    handle.error(f"{f.__name__} выбросила {type(e).__name__}: {e}")
                    raise
            else:
                handle.write(
                    f"[INFO] Вызов {f.__name__} c args = {args}, kwargs = {kwargs}\n"
                )
                try:
                    result = f(*args, **kwargs)
                    handle.write(f"[INFO] {f.__name__} вернула {result}\n")
                    return result
                except Exception as e:
                    handle.write(
                        f"[ERROR] {f.__name__} выбросила {type(e).__name__}: {e}\n"
                    )
                    raise

        return inner

    if func is None:
        return decorator
    else:
        return decorator(func)


@logger_for_demo(handle=quadratic_logger)
def solve_quadratic(a, b, c):
    """
    Решает квадратное уравнение ax² + bx + c = 0.

    Args:
        a - коэффициент перед x^2
        b - коэффициент перед x
        c - свободный член

    Returns:
        tuple: кортеж со статусом ошибки или инф, описанием, и корень если есть в противном NONE,
        Например ("CRITICAL", "Бесконечное множество решений (0 = 0)", None)
    """

    if not all(isinstance(x, (int, float)) for x in [a, b, c]):
        raise TypeError(
            f"Все коэффициенты должны быть числами, получено: a={type(a)}, b={type(b)}, c={type(c)}"
        )

    if a == 0 and b == 0:
        if c == 0:
            return ("CRITICAL", "Бесконечное множество решений (0 = 0)", None)
        else:
            return ("CRITICAL", f"Нет решений ({c} = 0 невозможно)", None)

    if a == 0:
        root = -c / b
        return ("INFO", f"Линейное уравнение, один корень", [root])

    discriminant = b * b - 4 * a * c

    if discriminant < 0:
        return (
            "WARNING",
            f"Дискриминант < 0 ({discriminant}), нет действительных корней",
            None,
        )

    if discriminant == 0:
        root = -b / (2 * a)
        return ("INFO", "Один корень (дискриминант = 0)", [root])
    else:
        sqrt_d = math.sqrt(discriminant)
        root1 = (-b + sqrt_d) / (2 * a)
        root2 = (-b - sqrt_d) / (2 * a)
        return ("INFO", "Два корня", [root1, root2])

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


def demo():
    print("=" * 60)

    print("\nПолучение курсов валют (get_currencies):")
    try:
        result = get_currencies(["USD", "EUR"])
        print(f"Результат: {result}")
    except Exception as e:
        print(f"Ошибка: {type(e).__name__}: {e}")

    print("\nРешение квадратного уравнения (solve_quadratic):")
    print("\nINFO: два корня:")
    solve_quadratic(1, -5, 6)

    print("\nWARNING: дискриминант < 0:")
    solve_quadratic(1, 0, 1)

    print("\nERROR: некорректные данные:")
    try:
        solve_quadratic("abc", 1, 1)
    except TypeError as e:
        print(f"Перехвачено исключение: {e}")

    print("\nCRITICAL:")
    solve_quadratic(0, 0, 5)

    print("\nФайловое логирование (currency.log):")
    try:
        result = get_currencies_file_logged(["USD"])
        print(f"Результат: {result}")
        print("Логи записаны в файл currency.log")
    except Exception as e:
        print(f"Ошибка: {type(e).__name__}: {e}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo()
    else:
        unittest.main(verbosity=2)
