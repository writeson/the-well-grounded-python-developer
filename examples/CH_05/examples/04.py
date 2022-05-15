
import functools
from time import sleep, time


def timing_decorator(func):
    @functools.wraps(func)
    def wrapper(delay):
        start_time = time()
        print("starting timing")
        result = func(delay)
        print(f"task elapsed time: {time() - start_time}")
        return result
    return wrapper


def complex_task_1(delay):
    sleep(delay)
    return "task done"


@timing_decorator
def complex_task_2(delay):
    sleep(delay)
    return "task done"


def main():
    delay = 1.5

    new_complex_task = timing_decorator(complex_task_1)
    print(new_complex_task(delay))
    print()
    print(complex_task_2(delay))


if __name__ == "__main__":
    main()
