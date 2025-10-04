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


def fact_iterative(n: int) -> int:
    """Итеративный факториал"""
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res


def benchmark(func, n, repeat=5):
    """Возвращает среднее время выполнения func(n)"""
    times = timeit.repeat(lambda: func(n), number=1, repeat=repeat)
    return min(times)



def main():
    # фиксированный набор данных
    random.seed(42)
    test_data = list(range(10, 300, 10))

    res_cache_iterative = []
    res_iterative = []

    for n in test_data:
        cache_fact_iterative.cache_clear()
        cache_fact_iterative(n)
        res_iterative.append(benchmark(fact_iterative, n))
        res_cache_iterative.append(benchmark(cache_fact_iterative, n))

    # Визуализация
    plt.plot(test_data, res_cache_iterative, label="cache iterative")
    plt.plot(test_data, res_iterative, label="iterative")
    plt.xlabel("n")
    plt.ylabel("Время (сек)")
    plt.title("cache iterative and iterative")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
