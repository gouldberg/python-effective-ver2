#!/usr/bin/env PYTHONHASHSEED=1234 python3

import logging

# ------------------------------------------------------------------------------
# simple example
# ------------------------------------------------------------------------------

try:
    class MyError(Exception):
        pass
    
    def my_generator():
        yield 1
        yield 2
        yield 3
    
    it = my_generator()
    print(next(it))  # Yield 1
    print(next(it))  # Yield 2
    print(it.throw(MyError('test error')))
except:
    logging.exception('Expected')
else:
    assert False

# -->
# logging.exception('Expected') is called
# also, it.throw() calls 


# ------------------------------------------------------------------------------
# it.throw() catch exception and may provide bi-directional communication channel
# ------------------------------------------------------------------------------

def my_generator():
    yield 1

    try:
        yield 2
    except MyError:
        print('Got MyError!')
    else:
        yield 3

    yield 4

it = my_generator()

print(next(it))  # Yield 1

print(next(it))  # Yield 2

# not 'test error' but 'Got MyError!' 
print(it.throw(MyError('test error')))

# --> catch exception. This may provide bi-directional communication channel

# main__.MyError: test error
print(it.throw(MyError('test error')))


# ----------
# again
it = my_generator()

print(next(it))  # Yield 1
print(next(it))  # Yield 2
print(next(it))  # Yield 3

# main__.MyError: test error
print(it.throw(MyError('test error')))


# ----------
# again
it = my_generator()

print(next(it))  # Yield 1
print(next(it))  # Yield 2
print(next(it))  # Yield 3
print(next(it))  # Yield 4

# main__.MyError: test error
print(it.throw(MyError('test error')))


# ------------------------------------------------------------------------------
# program to reset timer at given time
# ------------------------------------------------------------------------------

class Reset(Exception):
    pass

def timer(period):
    current = period
    while current:
        current -= 1
        try:
            yield current
        except Reset:
            current = period

# True: back to 3.
RESETS = [
    False, False, False, True, False, True, False,
    False, False, False, False, False, False, False]

def check_for_reset():
    # Poll for external event
    return RESETS.pop(0)

def announce(remaining):
    print(f'{remaining} ticks remaining')

def run():
    it = timer(4)    
    while True:
        try:
            if check_for_reset():
                # it.throw() here.
                current = it.throw(Reset())
            else:
                current = next(it)
        except StopIteration:
            break
        else:
            announce(current)

run()


# ------------------------------------------------------------------------------
# program to reset timer at given time, more readable
# Not use it.throw()
# Use iterable container object
# ------------------------------------------------------------------------------

# Iterable container object (Timer generator)
class Timer:
    def __init__(self, period):
        self.current = period
        self.period = period

    def reset(self):
        self.current = self.period

    def __iter__(self):
        while self.current:
            self.current -= 1
            yield self.current

RESETS = [
    False, False, True, False, True, False,
    False, False, False, False, False, False, False]

def run():
    timer = Timer(4)
    # Timer class is iterable
    for current in timer:
        if check_for_reset():
            timer.reset()
        announce(current)

run()
