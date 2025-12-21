from concurrent.futures import ThreadPoolExecutor
from functools import partial
try:
    from .Iter_5 import integrate_nogil
except ImportError:
    from Iter_5 import integrate_nogil


def integrate_asyncTH_nogil(a: float, b: float, *, n_jobs: int = 6 , n_iter: int = 1000) -> float:
    """
    Функция приближенно вычисляет площадь под графиком (определенный интеграл) на интервале [a,b]
    Разбивает интервал на n_jobs подинтервалов и вычисляет интеграл на каждом параллельно, используя noGil версию.
    Args:
        a - левая граница
        b - правая граница
        n_jobs - кол-во потоков
        n_iter - количество разбиений
    Returns:
        float: приближённое значение интеграла
    """
    with ThreadPoolExecutor(max_workers=n_jobs) as executor:
        spawn = partial(executor.submit, integrate_nogil, n_iter=n_iter // n_jobs)

        step = (b - a) / n_jobs

        fs = [spawn(a + i * step, a + (i + 1) * step) for i in range(n_jobs)]

        total_result = sum(f.result() for f in fs)

    return total_result