#!/usr/bin/env PYTHONHASHSEED=1234 python3

from random import randint

# profile (pure python): large overhead.
# use cProfile
from cProfile import Profile
from pstats import Stats

from sys import stdout as STDOUT

from bisect import bisect_left


# ------------------------------------------------------------------------------
# profiling basics
# ------------------------------------------------------------------------------

def insertion_sort(data):
    result = []
    for value in data:
        insert_value(result, value)
    return result


# this includes list.insert
def insert_value(array, value):
    for i, existing in enumerate(array):
        if existing > value:
            array.insert(i, value)
            return
    array.append(value)


# ----------
# test function
max_size = 10**4
data = [randint(0, max_size) for _ in range(max_size)]
test = lambda: insertion_sort(data)


# ----------
# profiling the test functions
profiler = Profile()
profiler.runcall(test)


# ----------
# statistics from profiler
stats = Stats(profiler)
stats = Stats(profiler, stream=STDOUT)

stats.strip_dirs()
stats.sort_stats('cumulative')


# ncalls:  num of test function is called during profiling 
# tottime: secs of function executing excluding calling others.
# tottime percall = tottime / ncalls

# 1.419 secs.
stats.print_stats()

# --> function 'insert_value' is consuming CPU


# ------------------------------------------------------------------------------
# use bisect_left instead of list.insert
# ------------------------------------------------------------------------------

def insert_value(array, value):
    i = bisect_left(array, value)
    array.insert(i, value)


profiler = Profile()
profiler.runcall(test)

stats = Stats(profiler, stream=STDOUT)
stats.strip_dirs()
stats.sort_stats('cumulative')

# 0.036secs
stats.print_stats()


# ------------------------------------------------------------------------------
# print_callers()
# show called and calling function
# ------------------------------------------------------------------------------

def my_utility(a, b):
    c = 1
    for i in range(100):
        c += a * b

def first_func():
    for _ in range(1000):
        my_utility(4, 5)

def second_func():
    for _ in range(10):
        my_utility(1, 3)

def my_program():
    for _ in range(20):
        first_func()
        second_func()


profiler = Profile()
profiler.runcall(my_program)
stats = Stats(profiler, stream=STDOUT)
stats.strip_dirs()
stats.sort_stats('cumulative')


# my_utility is consuming most CPU time, but details is not shown.
stats.print_stats()


# ----------
# print_callers() show called and calling function
stats = Stats(profiler, stream=STDOUT)
stats.strip_dirs()
stats.sort_stats('cumulative')

# left:  called func
# right:  calling func
# first_func is calling my_utility mostly.
stats.print_callers()

