def dict_bin_tree(height: int, root_value = 10, l_b = None, r_b = None) -> dict:
    """Функция рекурсивно генирирующая полное бинарное дерево с заданной высотой для unittest.

    height: int - высота бинарного дерева
    root_value: int - изначальное значение для корня с индексом 0
    l_b - функция для левого корня
    r_b - функfrom Tests_Pylab3 import custom_right, custom_leftиця для правого корня
    """

    def alexander(root_value: int) -> int:
        """Вычисляет значение левого корня по формуле: (3 * x + 1).

            root_value - значение корня с индексом 0
            """
        return root_value * 3 + 1

    def lesnitskiy(root_value: int) -> int:
        """Вычисляет значение правого корня по формуле: (3 * x - 1).

            root_value - значение корня с индексом 0
            """
        return 3 * root_value - 1

    def bin_tree(height, root = 0, l_b = None, r_b = None, h_actually = 1):
        """ Функция рекурсивно генирирующая полное бинарное дерево с заданной высотой.

        height: int - высота бинарного дерева
        root: int - номер корня
        l_b - функция для левого корня
        r_b - функиця для правого корня
        h_actually: int - актуальная высота какого-то корня
        """

        if h_actually < height:
            actually_value = dictionary[root]

            # Для левого корня
            left_value = l_b(actually_value)
            left_index = 2 * root + 1
            dictionary[left_index] = left_value
            bin_tree(height, left_index, l_b, r_b, h_actually + 1)

            # Для правого корня
            right_value = r_b(actually_value)
            right_index = 2 * root + 2
            dictionary[right_index] = right_value
            bin_tree(height, right_index, l_b, r_b, h_actually + 1)

    if l_b is None:
        l_b = alexander
    if r_b is None:
        r_b = lesnitskiy

    dictionary: dict[int, int] = dict()
    dictionary[0] = root_value
    bin_tree(height, l_b = l_b, r_b = r_b)
    sorted_dict = sorted(dictionary.items())
    dictionary.clear()
    dictionary.update(sorted_dict)
    return dictionary