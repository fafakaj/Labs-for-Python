import math


def integrate(f, a:float, b:float, *, n_iter:int = 1000) -> float:
    """
    Функция приближенно вычисляет площадь под графиком (определенный интеграл) на интервале [a,b]
    Args:
        f - функция, под которой вычисляется площадь
        a - левая граница
        b - правая граница
        n_iter - количество разбиений
    Return:
        float: приближённое значение интеграла
    """
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc

def test_integral_polynomial():
    """Проверяет правильный расчёт известного интеграла x^2 от 0 до 3."""
    result = integrate(lambda x: x ** 2, 0, 3, n_iter=10000)
    expected = 9.0
    assert abs(result - expected) < 0.1

def test_integral_trigonometric():
    """Проверяет правильный расчёт известного интеграла sin(x) от 0 до pi."""
    result = integrate(math.sin, 0, math.pi, n_iter=10000)
    expected = 2.0
    assert abs(result - expected) < 0.01

def test_accuracy():
    """Проверяет улучшение точности при увеличении числа итераций."""
    func_to_test = math.cos
    a, b = 0, math.pi
    expected = 0.0

    result_low = integrate(func_to_test, a, b, n_iter=100)
    result_high = integrate(func_to_test, a, b, n_iter=10000)

    assert abs(result_low - expected) > abs(result_high - expected)







