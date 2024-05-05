#!/usr/bin/env PYTHONHASHSEED=1234 python3

import time

from collections import deque
from threading import Thread
from threading import Lock

from queue import Queue


# ------------------------------------------------------------------------------
# factory linear pipeline process by queue and threading
# ------------------------------------------------------------------------------

# ----------
# individual processes
def download(item):
    return item

def resize(item):
    return item

def upload(item):
    return item


# ----------
# queue put and get with threading.lock()
class MyQueue:
    def __init__(self):
        self.items = deque()
        self.lock = Lock()

    def put(self, item):
        with self.lock:
            self.items.append(item)

    def get(self):
        with self.lock:
            return self.items.popleft()


# ----------
class Worker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0

    def run(self):
        # Here indefinite loop (no signal to stop)
        while True:
            self.polled_count += 1
            try:
                item = self.in_queue.get()
            except IndexError:
                time.sleep(0.01)  # No work to do
            except AttributeError:
                # The magic exit signal
                return
            else:
                # get result from process
                result = self.func(item)
                self.out_queue.put(result)
                self.work_done += 1


# ----------
download_queue = MyQueue()
resize_queue = MyQueue()
upload_queue = MyQueue()
done_queue = MyQueue()

threads = [
    Worker(download, download_queue, resize_queue),
    Worker(resize, resize_queue, upload_queue),
    Worker(upload, upload_queue, done_queue),
]


# ----------
for thread in threads:
    thread.start()

for _ in range(1000):
    # just put object()
    download_queue.put(object())


while len(done_queue.items) < 1000:
    # Do something useful while waiting
    time.sleep(0.1)


# Stop all the threads by causing an exception in their run methods.
for thread in threads:
    thread.in_queue = None
    thread.join()


processed = len(done_queue.items)

polled = sum(t.polled_count for t in threads)

print(f'Processed {processed} items after '
      f'polling {polled} times')


# --> this implementation's problem
# 1. busy wait
# 2. blocking operation
# 3. memory consumption


# ------------------------------------------------------------------------------
# queue.Queue:  better for robust pipeline (blocking operation, buffer size, join, etc.)
#
#   - not require busy wait by blocking get method until new data is provided
# ------------------------------------------------------------------------------

my_queue = Queue()

def consumer():
    print('Consumer waiting')
    my_queue.get()              # Runs after put() below
    print('Consumer done')

thread = Thread(target=consumer)
thread.start()

# --> 'Consumer done' is not printed, Queue.get() is waiting


# now provide data
print('Producer putting')
my_queue.put(object())          # Runs before get() above

# --> now 'Consumer done' is printed


print('Producer done')
thread.join()


# ------------------------------------------------------------------------------
# queue.Queue:
#   - by specifying buffer size, if buffer is filled, put is blocked
# ------------------------------------------------------------------------------

my_queue = Queue(1)             # Buffer size of 1

def consumer():
    time.sleep(0.1)             # Wait
    my_queue.get()              # Runs second
    print('Consumer got 1')
    my_queue.get()              # Runs fourth
    print('Consumer got 2')
    print('Consumer done')

thread = Thread(target=consumer)
thread.start()


my_queue.put(object())          # Runs first
print('Producer put 1')

# --> 'Consumer got 2' is not printed, since buffer is filled.

# now second input
my_queue.put(object())          # Runs third
print('Producer put 2')

print('Producer done')
thread.join()


# ------------------------------------------------------------------------------
# queue.Queue:
#   - track process by task_done method, do not require polling done queue
# ------------------------------------------------------------------------------

in_queue = Queue()

def consumer():
    print('Consumer waiting')
    work = in_queue.get()       # Done second
    print('Consumer working')
    # Doing work
    print('Consumer done')
    in_queue.task_done()        # Done third

thread = Thread(target=consumer)
thread.start()


print('Producer putting')
in_queue.put(object())         # Done first


# in_queue.join() can not be finished until all task in queue is called task_done() 
print('Producer waiting')
in_queue.join()                # Done fourth


print('Producer done')
thread.join()


# ------------------------------------------------------------------------------
# closable queue and stoppable worker
# ------------------------------------------------------------------------------

class ClosableQueue(Queue):
    SENTINEL = object()

    def close(self):
        self.put(self.SENTINEL)

    def __iter__(self):
        while True:
            item = self.get()
            try:
                if item is self.SENTINEL:
                    return  # Cause the thread to exit
                yield item
            finally:
                self.task_done()


class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)


# ----------
download_queue = ClosableQueue()
resize_queue = ClosableQueue()
upload_queue = ClosableQueue()
done_queue = ClosableQueue()

threads = [
    StoppableWorker(download, download_queue, resize_queue),
    StoppableWorker(resize, resize_queue, upload_queue),
    StoppableWorker(upload, upload_queue, done_queue),
]


for thread in threads:
    thread.start()

for _ in range(1000):
    download_queue.put(object())


# ----------
# join queue and wait until finishing, following order of process
# (download -> resize -> upload)

download_queue.close()
download_queue.join()

resize_queue.close()
resize_queue.join()

upload_queue.close()
upload_queue.join()

print(done_queue.qsize(), 'items finished')

for thread in threads:
    thread.join()


# ------------------------------------------------------------------------------
# extend to use multiple producer threads to each process
#   --> improve I/O parallel and speed-up
#
# Queue works good for linear pipeline such as this example,
# but using coroutine will be better (refer to 060)
# ------------------------------------------------------------------------------

def start_threads(count, *args):
    threads = [StoppableWorker(*args) for _ in range(count)]
    for thread in threads:
        thread.start()
    return threads

def stop_threads(closable_queue, threads):
    for _ in threads:
        closable_queue.close()

    closable_queue.join()

    for thread in threads:
        thread.join()


# ----------
download_queue = ClosableQueue()
resize_queue = ClosableQueue()
upload_queue = ClosableQueue()
done_queue = ClosableQueue()

download_threads = start_threads(
    3, download, download_queue, resize_queue)

resize_threads = start_threads(
    4, resize, resize_queue, upload_queue)

upload_threads = start_threads(
    5, upload, upload_queue, done_queue)

for _ in range(1000):
    download_queue.put(object())

stop_threads(download_queue, download_threads)
stop_threads(resize_queue, resize_threads)
stop_threads(upload_queue, upload_threads)

print(done_queue.qsize(), 'items finished')
