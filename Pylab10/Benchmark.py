import timeit
import math
from Iter_1 import integrate
from Iter_2 import integrate_async_threads
from Iter3.Iter_3 import integrate_async_processes
from Iter3.def_func_3 import complex_test_func
from Iter4.Iter_4 import integrate_cython
from Iter5.integrate_asyncTH_nogil import integrate_asyncTH_nogil
from Iter4.integrate_asyncPR import integrate_asyncPR


test_a, test_b = 1, 150
n_iter=10000
amount_runs = 100
test_func = lambda x: (
    (math.gamma(x + 2) * math.sin(x ** 2) * math.exp(math.log(x + 1) ** 2))
    / (math.factorial(max(1, int(x))) * math.sqrt(x ** 3 + 1))
)


def benchmark_integration():
    """
    Функция, считающая среднее время вычисления интреграла.
    """
    print("--- Время выполнения integrate ---")

    time = timeit.timeit(
        lambda: integrate(test_func, test_a, test_b, n_iter=n_iter),
        number=amount_runs
        )
    avg_time = time / amount_runs
    print(f"Среднее время выполнения: {avg_time:.8f} секунд")

def benchmark_integration_cython():
    """
    Функция, считающая среднее время вычисления интреграла на оптимизированном языке.
    """
    print("\n--- Время выполнения integrate_cython ---")

    time = timeit.timeit(
        lambda: integrate_cython(test_a, test_b, n_iter=n_iter),
        number=amount_runs
    )
    avg_time = time / amount_runs
    print(f"Среднее время выполнения: {avg_time:.8f} секунд")

def benchmark_async_integration_threads():
    """
    Функция, считающая среднее время вычисления интреграла, разделяя все на потоки.
    """
    print("\n--- Время выполнения integrate_async_threads ---")
    n_jobs_test = [2, 4, 6, 8, 10, 12]

    for n_jobs in n_jobs_test:
        time = timeit.timeit(
            lambda: integrate_async_threads(test_func, test_a, test_b, n_jobs=n_jobs, n_iter=n_iter),
            number=amount_runs
        )
        avg_time = time / amount_runs
        print(f"(n_jobs = {n_jobs}): Среднее время выполнения: {avg_time:.6f} секунд")

def benchmark_async_integration_processes():
    """
    Функция, считающая среднее время вычисления интреграла, разделяя все на процессы.
    """
    print("\n--- Время выполнения integrate_async_processes ---")
    n_jobs_test = [2, 4, 6, 8]

    for n_jobs in n_jobs_test:
        time = timeit.timeit(
            lambda: integrate_async_processes(complex_test_func, test_a, test_b, n_jobs=n_jobs, n_iter=n_iter),
            number=amount_runs
        )
        avg_time = time / amount_runs
        print(f"(n_jobs = {n_jobs}): Среднее время выполнения: {avg_time:.6f} секунд")

def benchmark_asyncTH_integration_nogil():
    """
    Функция, считающая среднее время вычисления интреграла, написанная с помощью оптимизированного языка и разделяющая все на потоки, при помощи noGIL.
    """
    print("\n--- Время выполнения integrate_asyncTH_nogil ---")
    n_jobs_test = [2, 4, 6]

    for n_jobs in n_jobs_test:
        time = timeit.timeit(
            lambda: integrate_asyncTH_nogil(test_a, test_b, n_jobs=n_jobs, n_iter=n_iter),
            number=amount_runs
        )
        avg_time = time / amount_runs
        print(f"(n_jobs = {n_jobs}): Среднее время выполнения: {avg_time:.6f} секунд")

def benchmark_asyncPR_integration():
    """
    Функция, считающая среднее время вычисления интреграла, написанная с помощью оптимизированного языка и разделяющая все на процессы.
    """
    print("\n--- Время выполнения integrate_asyncPR ---")
    n_jobs_test = [2, 4, 6]

    for n_jobs in n_jobs_test:
        time = timeit.timeit(
            lambda: integrate_asyncPR(test_a, test_b, n_jobs=n_jobs, n_iter=n_iter),
            number=amount_runs
        )
        avg_time = time / amount_runs
        print(f"(n_jobs = {n_jobs}): Среднее время выполнения: {avg_time:.6f} секунд")


if __name__ == "__main__":
    benchmark_integration()
    benchmark_integration_cython()
    benchmark_async_integration_threads()
    benchmark_async_integration_processes()
    benchmark_asyncTH_integration_nogil()
    benchmark_asyncPR_integration()


