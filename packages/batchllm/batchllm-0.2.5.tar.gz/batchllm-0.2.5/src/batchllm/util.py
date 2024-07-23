import threading
import time

class Counter:

    def __init__(self, start: int = 0) -> None:
        self.counter = start
        self.lock = threading.Lock()

    def __next__(self) -> int:
        with self.lock:
            i = self.counter
            self.counter += 1
        return i

    def reset(self) -> None:
        with self.lock:
            self.counter = 0

    def eval(self) -> None:
        with self.lock:
            return self.counter


def call_with_retry(func, *args, **kwargs):
    retry_num = 0
    retry_times = kwargs.pop("retry_times", 5)
    delay = kwargs.pop("delay", 0.1)
    exc_type = kwargs.pop("exc_type", BaseException)
    while True:
        try:
            return func(*args, **kwargs)
        except exc_type:
            retry_num += 1
            time.sleep(delay)
            if retry_num > retry_times:
                raise
