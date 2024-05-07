#!/usr/bin/env PYTHONHASHSEED=1234 python3

import collections
import timeit


# ------------------------------------------------------------------------------
# FIFO queue implemented by list
# ------------------------------------------------------------------------------

class Email:
    def __init__(self, sender, receiver, message):
        self.sender = sender
        self.receiver = receiver
        self.message = message


def get_emails():
    yield Email('foo@example.com', 'bar@example.com', 'hello1')
    yield Email('baz@example.com', 'banana@example.com', 'hello2')
    yield None
    yield Email('meep@example.com', 'butter@example.com', 'hello3')
    yield Email('stuff@example.com', 'avocado@example.com', 'hello4')
    yield None
    yield Email('thingy@example.com', 'orange@example.com', 'hello5')
    yield Email('roger@example.com', 'bob@example.com', 'hello6')
    yield None
    yield Email('peanut@example.com', 'alice@example.com', 'hello7')
    yield None


# ----------
EMAIL_IT = get_emails()


class NoEmailError(Exception):
    pass


def try_receive_email():
    # Returns an Email instance or raises NoEmailError
    try:
        email = next(EMAIL_IT)
    except StopIteration:
        email = None

    if not email:
        raise NoEmailError

    print(f'Produced email: {email.message}')
    return email


# ----------
# producer append email in queue (this is list)
def produce_emails(queue):
    while True:
        try:
            email = try_receive_email()
        except NoEmailError:
            return
        else:
            queue.append(email)  # Producer


# consumer pop email from queue (this is list)
def consume_one_email(queue):
    if not queue:
        return
    email = queue.pop(0)  # Consumer
    # Index the message for long-term archival
    print(f'Consumed email: {email.message}')


# ----------
# queue is list now
def loop(queue, keep_running):
    while keep_running():
        produce_emails(queue)
        consume_one_email(queue)


def make_test_end():
    count=list(range(10))

    def func():
        if count:
            count.pop()
            return True
        return False

    return func


def my_end_func():
    pass


my_end_func = make_test_end()
loop([], my_end_func)


# ------------------------------------------------------------------------------
# benchmark for list append
# ------------------------------------------------------------------------------

def print_results(count, tests):
    avg_iteration = sum(tests) / len(tests)
    print(f'Count {count:>5,} takes {avg_iteration:.6f}s')
    return count, avg_iteration


def print_delta(before, after):
    before_count, before_time = before
    after_count, after_time = after
    growth = 1 + (after_count - before_count) / before_count
    slowdown = 1 + (after_time - before_time) / before_time
    print(f'{growth:>4.1f}x data size, {slowdown:>4.1f}x time')


# ----------
# list append
def list_append_benchmark(count):
    def run(queue):
        for i in range(count):
            queue.append(i)

    tests = timeit.repeat(
        setup='queue = []',
        stmt='run(queue)',
        globals=locals(),
        repeat=1000,
        number=1)

    return print_results(count, tests)


# ----------
baseline = list_append_benchmark(500)

for count in (1_000, 2_000, 3_000, 4_000, 5_000):
    print()
    comparison = list_append_benchmark(count)
    print_delta(baseline, comparison)


# -->
# base:  0.000037 sec
# 2.0x data size:  1.3x
# 4.0x data size:  2.5x
# 6.0x data size:  4.7x
# 8.0x data size:  6.6x
# 10.0x data size:  6.9x


# ------------------------------------------------------------------------------
# benchmark for list pop : O(n^2)
# ------------------------------------------------------------------------------

def list_pop_benchmark(count):
    def prepare():
        return list(range(count))

    def run(queue):
        while queue:
            queue.pop(0)

    tests = timeit.repeat(
        setup='queue = prepare()',
        stmt='run(queue)',
        globals=locals(),
        repeat=1000,
        number=1)

    return print_results(count, tests)


# ----------
baseline = list_pop_benchmark(500)

for count in (1_000, 2_000, 3_000, 4_000, 5_000):
    print()
    comparison = list_pop_benchmark(count)
    print_delta(baseline, comparison)


# -->
# base:  0.000053 sec
# 2.0x data size:  1.7x
# 4.0x data size:  4.0x
# 6.0x data size:  7.5x
# 8.0x data size:  12.5x
# 10.0x data size:  22.4x


# ------------------------------------------------------------------------------
# use deque (this is FIFO)
# ------------------------------------------------------------------------------

def consume_one_email(queue):
    if not queue:
        return
    email = queue.popleft()  # Consumer
    # Process the email message
    print(f'Consumed email: {email.message}')


def my_end_func():
    pass

my_end_func = make_test_end()

EMAIL_IT = get_emails()

loop(collections.deque(), my_end_func)


# ------------------------------------------------------------------------------
# benchmark for deque for append
# ------------------------------------------------------------------------------

def deque_append_benchmark(count):
    def prepare():
        return collections.deque()

    def run(queue):
        for i in range(count):
            queue.append(i)

    tests = timeit.repeat(
        setup='queue = prepare()',
        stmt='run(queue)',
        globals=locals(),
        repeat=1000,
        number=1)
    return print_results(count, tests)


# -----------
baseline = deque_append_benchmark(500)

for count in (1_000, 2_000, 3_000, 4_000, 5_000):
    print()
    comparison = deque_append_benchmark(count)
    print_delta(baseline, comparison)


# -->
# base:  0.000041 sec
# 2.0x data size:  1.0x
# 4.0x data size:  1.9x
# 6.0x data size:  2.9x
# 8.0x data size:  3.8x
# 10.0x data size: 4.7x


# ------------------------------------------------------------------------------
# benchmark for deque for pop
# ------------------------------------------------------------------------------

def dequeue_popleft_benchmark(count):
    def prepare():
        return collections.deque(range(count))

    def run(queue):
        while queue:
            queue.popleft()

    tests = timeit.repeat(
        setup='queue = prepare()',
        stmt='run(queue)',
        globals=locals(),
        repeat=1000,
        number=1)

    return print_results(count, tests)


# -----------
baseline = dequeue_popleft_benchmark(500)

for count in (1_000, 2_000, 3_000, 4_000, 5_000):
    print()
    comparison = dequeue_popleft_benchmark(count)
    print_delta(baseline, comparison)


# -->
# base:  0.000031 sec
# 2.0x data size:  1.1x
# 4.0x data size:  2.2x
# 6.0x data size:  3.7x
# 8.0x data size:  4.1x
# 10.0x data size: 5.1x
