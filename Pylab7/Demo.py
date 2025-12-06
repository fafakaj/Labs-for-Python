import sys
import functools
import logging
import math


quadratic_logger = logging.getLogger("quadratic")
quadratic_logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)

if not quadratic_logger.handlers:
    quadratic_logger.addHandler(console_handler)


def logger_for_demo(func=None, *, handle=sys.stdout):
    def decorator(f):
        @functools.wraps(f)
        def inner(*args, **kwargs):
            is_logger = hasattr(handle, "info") and callable(getattr(handle, "info"))

            if is_logger:
                handle.info(f"Вызов {f.__name__} c args = {args}, kwargs = {kwargs}")
                try:
                    result = f(*args, **kwargs)
                    if isinstance(result, tuple) and len(result) == 3:
                        status, msg, roots = result
                        if status == "INFO":
                            handle.info(f"{f.__name__}: {msg}, корни: {roots}")
                        elif status == "WARNING":
                            handle.warning(f"{f.__name__}: {msg}")
                        elif status == "CRITICAL":
                            handle.critical(f"{f.__name__}: {msg}")
                        return roots
                    else:
                        handle.info(f"{f.__name__} вернула {result}")
                    return result
                except Exception as e:
                    handle.error(f"{f.__name__} выбросила {type(e).__name__}: {e}")
                    raise
            else:
                handle.write(
                    f"[INFO] Вызов {f.__name__} c args = {args}, kwargs = {kwargs}\n"
                )
                try:
                    result = f(*args, **kwargs)
                    handle.write(f"[INFO] {f.__name__} вернула {result}\n")
                    return result
                except Exception as e:
                    handle.write(
                        f"[ERROR] {f.__name__} выбросила {type(e).__name__}: {e}\n"
                    )
                    raise

        return inner

    if func is None:
        return decorator
    else:
        return decorator(func)


@logger_for_demo(handle=quadratic_logger)
def solve_quadratic(a, b, c):
    """
    Решает квадратное уравнение ax² + bx + c = 0.

    Args:
        a - коэффициент перед x^2
        b - коэффициент перед x
        c - свободный член

    Returns:
        tuple: кортеж со статусом ошибки или инф, описанием, и корень если есть в противном NONE,
        Например ("CRITICAL", "Бесконечное множество решений (0 = 0)", None)
    """

    if not all(isinstance(x, (int, float)) for x in [a, b, c]):
        raise TypeError(
            f"Все коэффициенты должны быть числами, получено: a={type(a)}, b={type(b)}, c={type(c)}"
        )

    if a == 0 and b == 0:
        if c == 0:
            return ("CRITICAL", "Бесконечное множество решений (0 = 0)", None)
        else:
            return ("CRITICAL", f"Нет решений ({c} = 0 невозможно)", None)

    if a == 0:
        root = -c / b
        return ("INFO", f"Линейное уравнение, один корень", [root])

    discriminant = b * b - 4 * a * c

    if discriminant < 0:
        return (
            "WARNING",
            f"Дискриминант < 0 ({discriminant}), нет действительных корней",
            None,
        )

    if discriminant == 0:
        root = -b / (2 * a)
        return ("INFO", "Один корень (дискриминант = 0)", [root])
    else:
        sqrt_d = math.sqrt(discriminant)
        root1 = (-b + sqrt_d) / (2 * a)
        root2 = (-b - sqrt_d) / (2 * a)
        return ("INFO", "Два корня", [root1, root2])
