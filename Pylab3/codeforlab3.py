def binary_tree(height, root = None, l_b = None, r_b = None, h_actually = 1) -> dict:
    """ Функция рекурсивно генирирующая полное бинарное дерево с заданной высотой.

    height: int - высота бинарного дерева
    root: int, None - значение корня
    l_b - функция для левого корня
    r_b - функиця для правого корня
    h_actually: int - актуальная высота какого-то корня
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

    if h_actually >= height:
        return {str(root): []}
    else:
        left = l_b(root)
        right = r_b(root)
        return {str(root): [binary_tree(height, left, l_b, r_b, h_actually + 1),
                            binary_tree(height, right, l_b, r_b, h_actually + 1)]}