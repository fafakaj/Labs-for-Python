def dict_bin_tree(height, l_b = None, r_b = None):
    """Функция рекурсивно генирирующая полное бинарное дерево с заданной высотой для unittest."""
    dictionary: dict[int, int] = {}
    root_value = 10


    def bin_tree(height, root = 0, l_b = None, r_b = None, h_actually = 1):
        """ Функция рекурсивно генирирующая полное бинарное дерево с заданной высотой.

        height - высота бинарного дерева
        root - номер корня
        l_b - функция для левого потомка
        r_b - функиця для правого потомка
        h_actually - актуальная высота какого-то корня
        """
        if h_actually < height:
            actually_value = dictionary[root]

            # Для левого потомка
            left_value = l_b(actually_value)
            left_index = 2 * root + 1
            dictionary[left_index] = left_value
            bin_tree(height, left_index, l_b, r_b, h_actually + 1)

            # Для правого потомка
            right_value = r_b(actually_value)
            right_index = 2 * root + 2
            dictionary[right_index] = right_value
            bin_tree(height, right_index, l_b, r_b, h_actually + 1)


    def alexander(root_value: int) -> int:
        """Вычисляет значение левого потомка по формуле: (3 * x + 1).

            root_value - значение родительского корня
            """
        return root_value * 3 + 1


    def lesnitskiy(root_value: int) -> int:
        """Вычисляет значение правого потомка по формуле: (3 * x - 1).

            root_value - значение родительского корня
            """
        return 3 * root_value - 1


    if l_b is None:
        l_b = alexander
    if r_b is None:
        r_b = lesnitskiy
    dictionary[0] = root_value
    bin_tree(height, l_b = l_b, r_b = r_b)
    sorted_dict = sorted(dictionary.items())
    dictionary.clear()
    dictionary.update(sorted_dict)
    return dictionary

def custom_left(x: int) -> int:
    return x + 1
# Пользовательская функция для значения левого корня

def custom_right(x: int) -> int:
    return x - 1
# Пользовательская функция для значения правого корня
