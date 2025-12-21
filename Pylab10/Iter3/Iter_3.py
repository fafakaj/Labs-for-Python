import concurrent.futures as ftres
from functools import partial
import math
from .def_func_3 import func_polynomial, func_complex

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from Iter_1 import integrate


def integrate_async_processes(f, a: float, b: float, *, n_jobs: int = 6 , n_iter: int = 1000) -> float:
    """
    Функция приближенно вычисляет площадь под графиком (определенный интеграл) на интервале [a,b]
    Разбивает интервал на n_jobs подинтервалов и вычисляет интеграл на каждом параллельно.
    Args:
        f - функция, под которой вычисляется площадь
        a - левая граница
        b - правая граница
        n_jobs - кол-во потоков
        n_iter - количество разбиений
    Returns:
        float: приближённое значение интеграла
    """
    executor = ftres.ProcessPoolExecutor(max_workers=n_jobs)
    spawn = partial(executor.submit, integrate, f, n_iter = n_iter // n_jobs)

    step = (b - a) / n_jobs

    fs = [spawn(a + i * step, a + (i + 1) * step) for i in range(n_jobs)]

    total_result = sum(future.result() for future in ftres.as_completed(fs))
    return total_result


def test_async_integral_polynomial():
    """Проверяет правильный расчёт известного интеграла x^2 от 0 до 3 с 2 потоком."""
    result = integrate_async_processes(func_polynomial, 0, 3, n_jobs=2, n_iter=10000)
    expected = 9.0
    assert abs(result - expected) < 0.1

def test_async_integral_trigonometric():
    """Проверяет правильный расчёт известного интеграла sin(x) от 0 до pi с 4 потоками."""
    result = integrate_async_processes(math.sin, 0, math.pi, n_jobs=4, n_iter=10000)
    expected = 2.0
    assert abs(result - expected) < 0.01

def test_async_accuracy():
    """Проверяет, что результаты с 2 и 4 потоками близки (для одной и той же функции)."""
    a, b = 0, 2

    result_single = integrate_async_processes(func_complex, a, b, n_jobs=2, n_iter=10000)
    result_multi = integrate_async_processes(func_complex, a, b, n_jobs=4, n_iter=10000)

    assert abs(result_single - result_multi) < 0.001