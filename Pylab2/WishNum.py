def finding(target: int, leftbord: int, rightbord: int) -> tuple[int, int | None]:
    """function finding hidden number."""
    if leftbord <= target <= rightbord:
        count = 0
        while rightbord >= leftbord:
            middle = (rightbord + leftbord) // 2
            count += 1
            if target > middle:
                leftbord = middle + 1
            elif target < middle:
                rightbord = middle - 1
            else:
                return target, count
        return target, count
    else:
        return target, None