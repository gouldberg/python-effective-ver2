#!/usr/bin/env PYTHONHASHSEED=1234 python3

from collections import defaultdict


# ------------------------------------------------------------------------------
# key hook:  key is function
# For Python, hook is stateless function (with defined arguments and returns)
#   (Other language hook is implemented as class)
#   For Python, function is first class
#   Python can pass and refer to function and method
# ------------------------------------------------------------------------------

names = ['Socrates', 'Archimedes', 'Plato', 'Aristotle']

names.sort(key=len)

print(names)


# ------------------------------------------------------------------------------
# hook to defaultdict
# ------------------------------------------------------------------------------

# hook to return 0 as default
def log_missing():
    print('Key added')
    return 0


current = {'green': 12, 'blue': 3}

increments = [
    ('red', 5),
    ('blue', 17),
    ('orange', 9),
]

result = defaultdict(log_missing, current)
print('Before:', dict(result))

# add key and value
for key, amount in increments:
    result[key] += amount

print('After: ', dict(result))


# ------------------------------------------------------------------------------
# hook with stateful closure
#  --> test will be easier, since API is separated by hook and others
# ------------------------------------------------------------------------------

def increment_with_report(current, increments):
    added_count = 0

    def missing():
        nonlocal added_count  # Stateful closure
        added_count += 1
        return 0

    # defaultdict does not know hook 'missing' keep state.
    result = defaultdict(missing, current)
    for key, amount in increments:
        result[key] += amount

    return result, added_count


result, count = increment_with_report(current, increments)
assert count == 2
print(result)


# ------------------------------------------------------------------------------
# class as hook
# ------------------------------------------------------------------------------

# define class for encapsulate state to be tracked.
class CountMissing:
    def __init__(self):
        self.added = 0

    def missing(self):
        self.added += 1
        return 0


counter = CountMissing()

# pass class as hook
result = defaultdict(counter.missing, current)  # Method ref

for key, amount in increments:
    result[key] += amount

assert counter.added == 2

print(result)


# ------------------------------------------------------------------------------
# better way:  class as hook
# ------------------------------------------------------------------------------

class BetterCountMissing:
    def __init__(self):
        self.added = 0

    # here __call__
    # class instance is used as function arguments (like API hook)
    # stateful closure
    def __call__(self):
        self.added += 1
        return 0

counter = BetterCountMissing()

assert counter() == 0
assert callable(counter)


counter = BetterCountMissing()

# simple
result = defaultdict(counter, current)  # Relies on __call__

for key, amount in increments:
    result[key] += amount

assert counter.added == 2

print(result)
