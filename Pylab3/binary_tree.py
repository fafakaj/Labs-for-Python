from math import log2

dictionary: dict[int, int] = {}


def bin_tree(height, root):
    """function for generate binary tree"""
    h_actually: float = log2(root + 1) + 1
    if h_actually < height:

        # for left root
        dictionary[2 * root + 1] = dictionary[root] * 3 + 1
        bin_tree(height, 2 * root + 1)

        # for right root
        dictionary[2 * root + 2] = 3 * dictionary[root] - 1
        bin_tree(height, 2 * root + 2)


dictionary[0] = 10
bin_tree(3,0)

# sort by keys
sorted_dict = sorted(dictionary.items())
dictionary.clear()
dictionary.update(sorted_dict)
print(dictionary)