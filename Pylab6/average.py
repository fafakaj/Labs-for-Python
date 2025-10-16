import timeit
import matplotlib.pyplot as plt
import random


def iterative_bin_tree(height = 5, root = 10, l_b = lambda x: 3 * x + 1, r_b = lambda x: 3 * x - 1) -> dict:
    """ Функция итеративно генирирующая полное бинарное дерево с заданной высотой.

       height: int - высота бинарного дерева (0 - только корень, 1 - корень и два потомка и т.д.)
       root: int - значение корня
       l_b, r_b - функции для левого и правого корня
       Возвращает: словарь вида {str(): [левый корень, правый корень]}
       """
    n = 2 ** (height + 1) - 1
    mas = [None] * n
    mas[0] = root

    for i in range(0, n//2):
        current_val = mas[i]
        left_root = l_b(current_val)
        mas[2 * i + 1] = left_root
        right_root = r_b(current_val)
        mas[2 * i + 2] = right_root

    for j in range (len(mas) - 1, -1, -1):
        l = []
        if 2 * j + 2 < len(mas) and 2 * j + 1 < len(mas):
            l.append(mas[2 * j + 1])
            l.append(mas[2 * j + 2])
        mas[j] = {str(mas[j]): l}
    return mas[0]


def recursive_bin_tree(height, root = None, l_b = None, r_b = None, h_actually = 1) -> dict:
    """ Функция рекурсивно генирирующая полное бинарное дерево с заданной высотой.

    height: int - высота бинарного дерева
    root: int, None - значение корня
    l_b, r_b - функции для левого и правого корня
    Возвращает: словарь вида {str(): [левый корень, правый корень]}
    """

    def left_root(root: int) -> int:
        """Вычисляет значение левого корня по формуле: (3 * x + 1).

        root - значение родительского корня
        """
        return root * 3 + 1

    def right_root(root: int) -> int:
        """Вычисляет значение правого корня по формуле: (3 * x - 1).

        root - значения родительского корня
        """
        return 3 * root - 1


    if root is None:
        root = 10
    if l_b is None:
        l_b = left_root
    if r_b is None:
        r_b = right_root

    if h_actually > height:
        return {str(root): []}
    else:
        left = l_b(root)
        right = r_b(root)
        return {str(root): [recursive_bin_tree(height, left, l_b, r_b, h_actually + 1),
                            recursive_bin_tree(height, right, l_b, r_b, h_actually + 1)]}


def benchmark(func, n, repeat=5):
    """Возвращает среднее время выполнения func(n)"""
    times = timeit.repeat(lambda: func(n), number=1, repeat=repeat)
    return min(times)


def main():
    # фиксированный набор данных
    random.seed(42)
    test_data = list(range(15, 30))

    res_iterative = []
    res_recursive = []

    for n in test_data:
        res_recursive.append(benchmark(recursive_bin_tree, n))
        res_iterative.append(benchmark(iterative_bin_tree, n))

    # Визуализация
    plt.plot(test_data, res_iterative, label="iterative tree")
    plt.plot(test_data, res_recursive, label="recursive tree")
    plt.xlabel("n")
    plt.ylabel("Время (сек)")
    plt.title("average")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
