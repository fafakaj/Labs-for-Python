import timeit
import matplotlib.pyplot as plt
import random
from functools import cache

@cache
def cache_fact_iterative(n: int) -> int:
    """Кэшированный итеративный факториал"""
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res


@cache
def cache_fact_recursive(n: int) -> int:
    """Кэшированный рекурсивный факториал"""
    if n == 0:
        return 1
    return n * cache_fact_recursive(n - 1)


def benchmark(func, n, repeat=5):
    """Возвращает среднее время выполнения func(n)"""
    times = timeit.repeat(lambda: func(n), number=1, repeat=repeat)
    return min(times)



def main():
    # фиксированный набор данных
    random.seed(42)
    test_data = list(range(10, 300, 10))

    res_cache_iterative = []
    res_cache_recursive = []

    for n in test_data:
        cache_fact_recursive.cache_clear()
        cache_fact_recursive(n)
        cache_fact_iterative.cache_clear()
        cache_fact_iterative(n)
        res_cache_recursive.append(benchmark(cache_fact_recursive, n))
        res_cache_iterative.append(benchmark(cache_fact_iterative, n))

    # Визуализация
    plt.plot(test_data, res_cache_iterative, label="cache iterative")
    plt.plot(test_data, res_cache_recursive, label="cache recursive")
    plt.xlabel("n")
    plt.ylabel("Время (сек)")
    plt.title("cache iterative and cache recursive")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
