import time
import functools


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        val = func(*args, **kwargs)
        end_time = time.time()
        run_time = end_time - start_time
        print(f"Finished running {func.__name__} in {run_time:.4f} seconds.")
        return val
    return wrapper


@timer
def dothings(n_times):
    for _ in range(n_times):
        return sum((i ** 3 for i in range(100_000)))
dothings(100_000)

