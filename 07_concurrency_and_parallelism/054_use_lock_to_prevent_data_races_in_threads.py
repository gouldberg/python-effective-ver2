#!/usr/bin/env PYTHONHASHSEED=1234 python3

from threading import Barrier
from threading import Thread
from threading import Lock


# ------------------------------------------------------------------------------
# Race condition occurred in multi threads
# ------------------------------------------------------------------------------

class Counter:
    def __init__(self):
        self.count = 0

    def increment(self, offset):
        self.count += offset


def worker(sensor_index, how_many, counter):
    # barrier for the workers to synchronize when they start counting,
    # otherwise it's hard to get a race because the overhead of starting a thread is high.
    BARRIER.wait()
    for _ in range(how_many):
        # Read from the sensor
        # Nothing actually happens here,
        # but this is where the blocking I/O would go.
        counter.increment(1)


# ----------
num = 5

BARRIER = Barrier(num)
how_many = 10 ** num
counter = Counter()

threads = []

for i in range(num):
    thread = Thread(target=worker,
                    args=(i, how_many, counter))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

expected = how_many * num
found = counter.count

# but here, no difference .... (should be in race condition, but...)
print(f'Counter should be {expected}, got {found}')


# ------------------------------------------------------------------------------
# Lock to avoid race condition
# ------------------------------------------------------------------------------

class LockingCounter:
    def __init__(self):
        self.lock = Lock()
        self.count = 0

    def increment(self, offset):
        with self.lock:
            self.count += offset

num = 5

BARRIER = Barrier(num)
how_many = 10 ** num
counter = LockingCounter()

threads = []

for i in range(num):
    thread = Thread(target=worker,
                    args=(i, how_many, counter))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

expected = how_many * num
found = counter.count

print(f'Counter should be {expected}, got {found}')
