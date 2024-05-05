#!/usr/bin/env PYTHONHASHSEED=1234 python3


# ------------------------------------------------------------------------------
# animation with move and pause
# ------------------------------------------------------------------------------

def move(period, speed):
    for _ in range(period):
        yield speed

def pause(delay):
    for _ in range(delay):
        yield 0

# definition of movement
def animate():
    for delta in move(4, 5.0):
        yield delta
    for delta in pause(3):
        yield delta
    for delta in move(2, 3.0):
        yield delta

def render(delta):
    print(f'Delta: {delta:.1f}')
    # Move the images onscreen

def run(func):
    for delta in func():
        render(delta)

# ----------
run(animate)


# ------------------------------------------------------------------------------
# multiple and nested generators by yield from
# ------------------------------------------------------------------------------

# child generators: move, pause, move
# parent generator: 'animate_composed'

def animate_composed():
    yield from move(4, 5.0)
    yield from pause(3)
    yield from move(2, 3.0)

run(animate_composed)


# ------------------------------------------------------------------------------
# measure time to check of speed improvement
# ------------------------------------------------------------------------------

import timeit

def child():
    for i in range(1_000_000):
        yield i

# ----------
def slow():
    for i in child():
        yield i

baseline = timeit.timeit(
    stmt='for _ in slow(): pass',
    globals=globals(),
    number=200)

# 13.21 secs
print(f'Manual nesting {baseline:.2f}s')


# ----------
# use yield from
def fast():
    yield from child()

comparison = timeit.timeit(
    stmt='for _ in fast(): pass',
    globals=globals(),
    number=200)

# 11.50 secs
print(f'Composed nesting {comparison:.2f}s')


# 12.9% less time
reduction = -(comparison - baseline) / baseline

print(f'{reduction:.1%} less time')

