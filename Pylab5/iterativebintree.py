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
