import math

from .Iter_4 import integrate_cython


def test_integrate_complex():
    result = integrate_cython(1, 150, n_iter=1000)

    expected = 77018081401428.0
    accuracy = 1e-2

    assert abs(result - expected) < accuracy, f"Результат {result} не равен ожидаемому {expected}"
    assert not math.isnan(result)
    assert not math.isinf(result)
    assert isinstance(result, float)