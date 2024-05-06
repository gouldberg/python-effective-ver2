#!/usr/bin/env PYTHONHASHSEED=1234 python3

import random
import timeit
import functools

import math

from heapq import heappush, heapify, heappop


# ------------------------------------------------------------------------------
# queue is implemented by list
# ------------------------------------------------------------------------------

class Book:
    def __init__(self, title, due_date):
        self.title = title
        self.due_date = due_date


# if queue is list, it costs too much ...
def add_book(queue, book):
    queue.append(book)
    # sort by due_date, ascending
    queue.sort(key=lambda x: x.due_date, reverse=True)


# Exception class
class NoOverdueBooks(Exception):
    pass

def next_overdue_book(queue, now):
    if queue:
        book = queue[-1]
        if book.due_date < now:
            queue.pop()
            return book

    raise NoOverdueBooks


# ----------
# now queue is list ...
queue = []

add_book(queue, Book('Don Quixote', '2019-06-07'))
add_book(queue, Book('Frankenstein', '2019-06-05'))
add_book(queue, Book('Les Misérables', '2019-06-08'))
add_book(queue, Book('War and Peace', '2019-06-03'))

for i in range(len(queue)):
    print(queue[i].__dict__)


# ----------
# check overdue book
now = '2019-06-10'

for i in range(len(queue)):
    # popping
    found = next_overdue_book(queue, now)
    print(f'title: {found.title}   due: {found.due_date}')



# ----------
# removing
# if queue is list, it costs too much ...
def return_book(queue, book):
    queue.remove(book)

queue = []
book = Book('Treasure Island', '2019-06-04')

add_book(queue, book)
print('Before return:', [x.title for x in queue])

return_book(queue, book)
print('After return: ', [x.title for x in queue])


# ----------
# if returned all, NoOverdueBooks exception
try:
    next_overdue_book(queue, now)
except NoOverdueBooks:
    pass          # Expected
else:
    assert False  # Doesn't happen


# ------------------------------------------------------------------------------
# queue is implemented by list
# benchmark by timeit
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
# overdue
def list_overdue_benchmark(count):
    def prepare():
        to_add = list(range(count))
        random.shuffle(to_add)
        return [], to_add

    def run(queue, to_add):
        for i in to_add:
            queue.append(i)
            queue.sort(reverse=True)

        while queue:
            queue.pop()

    tests = timeit.repeat(
        setup='queue, to_add = prepare()',
        stmt=f'run(queue, to_add)',
        globals=locals(),
        repeat=100,
        number=1)

    return print_results(count, tests)


# ----------
# return
def list_return_benchmark(count):
    def prepare():
        queue = list(range(count))
        random.shuffle(queue)

        to_return = list(range(count))
        random.shuffle(to_return)

        return queue, to_return

    def run(queue, to_return):
        for i in to_return:
            queue.remove(i)

    tests = timeit.repeat(
        setup='queue, to_return = prepare()',
        stmt=f'run(queue, to_return)',
        globals=locals(),
        repeat=100,
        number=1)

    return print_results(count, tests)


# ----------
baseline = list_overdue_benchmark(500)

for count in (1_000, 1_500, 2_000):
    print()
    comparison = list_overdue_benchmark(count)
    print_delta(baseline, comparison)


# -->
# list overdue:
# 500:   baseline
# 1000:  2.4x
# 1500:  5.0x
# 2000:  9.7x

baseline = list_return_benchmark(500)

for count in (1_000, 1_500, 2_000):
    print()
    comparison = list_return_benchmark(count)
    print_delta(baseline, comparison)


# -->
# list return
# 500:   baseline
# 1000:  3.3x
# 1500:  7.8x
# 2000: 12.4x


# ------------------------------------------------------------------------------
# heapq (queue with priority)
# heapq.heappush
# O(log(n)) to add new element and remove minimum element
# ------------------------------------------------------------------------------

# add book use heappush
# not require to sort
def add_book(queue, book):
    heappush(queue, book)

class Book:
    def __init__(self, title, due_date):
        self.title = title
        self.due_date = due_date


# ----------
queue = []

add_book(queue, Book('Little Women', '2019-06-05'))

# TypeError
# because Book does not have method to compare.
add_book(queue, Book('The Time Machine', '2019-05-30'))


# ----------
# @functools.total_ordering  and  implement __lt__
@functools.total_ordering
class Book:
    def __init__(self, title, due_date):
        self.title = title
        self.due_date = due_date

    def __lt__(self, other):
        return self.due_date < other.due_date


queue = []

# now we can add book
add_book(queue, Book('Pride and Prejudice', '2019-06-01'))
add_book(queue, Book('The Time Machine', '2019-05-30'))
add_book(queue, Book('Crime and Punishment', '2019-06-06'))
add_book(queue, Book('Wuthering Heights', '2019-06-12'))

print([b.title for b in queue])


# ----------
# Since Book class is decorated by @functools.total_ordering and __lt__
# this can be sorted
queue = [
    Book('Pride and Prejudice', '2019-06-01'),
    Book('The Time Machine', '2019-05-30'),
    Book('Crime and Punishment', '2019-06-06'),
    Book('Wuthering Heights', '2019-06-12'),
]

queue.sort()

print([b.title for b in queue])


# ------------------------------------------------------------------------------
# heapq (queue with priority)
# heapq.heapify
# ------------------------------------------------------------------------------

queue = [
    Book('Pride and Prejudice', '2019-06-01'),
    Book('The Time Machine', '2019-05-30'),
    Book('Crime and Punishment', '2019-06-06'),
    Book('Wuthering Heights', '2019-06-12'),
]


# we can create heap by heapify from queue list
heapify(queue)

print([b.title for b in queue])


# ------------------------------------------------------------------------------
# heapq (queue with priority)
# heapq.heappop
# ------------------------------------------------------------------------------

def next_overdue_book(queue, now):
    if queue:
        book = queue[0]           # Most overdue first
        if book.due_date < now:
            heappop(queue)        # Remove the overdue book
            return book

    raise NoOverdueBooks


now = '2019-06-02'

book = next_overdue_book(queue, now)
print(book.title)

book = next_overdue_book(queue, now)
print(book.title)

try:
    next_overdue_book(queue, now)
except NoOverdueBooks:
    pass          # Expected
else:
    assert False  # Doesn't happen


# ------------------------------------------------------------------------------
# benchmark for overdue
# ------------------------------------------------------------------------------

def heap_overdue_benchmark(count):
    def prepare():
        to_add = list(range(count))
        random.shuffle(to_add)
        return [], to_add

    def run(queue, to_add):
        for i in to_add:
            heappush(queue, i)
        while queue:
            heappop(queue)

    tests = timeit.repeat(
        setup='queue, to_add = prepare()',
        stmt=f'run(queue, to_add)',
        globals=locals(),
        repeat=100,
        number=1)

    return print_results(count, tests)


baseline = heap_overdue_benchmark(500)

for count in (1_000, 1_500, 2_000):
    print(f'scale : {round(count/500 * math.log(count/500), 2)}')
    comparison = heap_overdue_benchmark(count)
    print_delta(baseline, comparison)


# -->
# heap overdue:
# 500:   baseline
# 1000:  1.3x
# 1500:  2.0x
# 2000:  2.6x


# ------------------------------------------------------------------------------
# return
# ------------------------------------------------------------------------------

@functools.total_ordering
class Book:
    def __init__(self, title, due_date):
        self.title = title
        self.due_date = due_date
        self.returned = False  # New field

    def __lt__(self, other):
        return self.due_date < other.due_date


def next_overdue_book(queue, now):
    while queue:
        book = queue[0]
        if book.returned:
            heappop(queue)
            continue

        if book.due_date < now:
            heappop(queue)
            return book

        break

    raise NoOverdueBooks


# ----------
queue = []

book = Book('Pride and Prejudice', '2019-06-01')
add_book(queue, book)

book = Book('The Time Machine', '2019-05-30')
add_book(queue, book)
book.returned = True

book = Book('Crime and Punishment', '2019-06-06')
add_book(queue, book)
book.returned = True

book = Book('Wuthering Heights', '2019-06-12')
add_book(queue, book)


# ----------
now = '2019-06-11'

book = next_overdue_book(queue, now)
assert book.title == 'Pride and Prejudice'

try:
    next_overdue_book(queue, now)
except NoOverdueBooks:
    pass          # Expected
else:
    assert False  # Doesn't happen


# ----------
def return_book(queue, book):
    book.returned = True

assert not book.returned

return_book(queue, book)

assert book.returned


# ------------------------------------------------------------------------------
# check heapq
# ------------------------------------------------------------------------------

import heapq

help(heapq)
