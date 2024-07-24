from functools import wraps
import time
from typing import Callable, Any


def retry(times: int = 5) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    assert times >= 1

    def wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            for i in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    print(f"{i} times tried")
                    if i == times:
                        raise
                    time.sleep(5 * i)

        return wrapped

    return wrapper
