import sys
import functools


def logger(func=None, *, handle=sys.stdout):
    def decorator(f):
        @functools.wraps(f)
        def inner(*args, **kwargs):
            is_logger = hasattr(handle, "info") and callable(getattr(handle, "info"))
            if is_logger:
                handle.info(
                    f"[INFO] Вызов {f.__name__} c args = {args}, kwargs = {kwargs}"
                )
                try:
                    result = f(*args, **kwargs)
                    handle.info(f"[INFO] {f.__name__} вернула {result}")
                    return result
                except Exception as e:
                    handle.error(
                        f"[ERROR] {f.__name__} выбросила {type(e).__name__}: {e}"
                    )
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