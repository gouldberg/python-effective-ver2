#!/usr/bin/env PYTHONHASHSEED=1234 python3


# ------------------------------------------------------------------------------
# normalize function
# ------------------------------------------------------------------------------

def normalize(numbers):
    # ----------
    # if numbers is iterator, this sum operation exhaust it.
    total = sum(numbers)
    # ----------
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result


visits = [15, 35, 80]
percentages = normalize(visits)
print(percentages)
assert sum(percentages) == 100.0


# ------------------------------------------------------------------------------
# save (write) numbers
# ------------------------------------------------------------------------------

path = '00_tmp/my_numbers.txt'

with open(path, 'w') as f:
    for i in (15, 35, 80):
        f.write('%d\n' % i)


# ------------------------------------------------------------------------------
# read numbers by iterator and normalize
# ------------------------------------------------------------------------------

# this function returns iterator
def read_visits(data_path):
    with open(data_path) as f:
        for line in f:
            yield int(line)

it = read_visits('00_tmp/my_numbers.txt')
percentages = normalize(it)
print(percentages)


# If you do again, iterator is already exhausted
it = read_visits('00_tmp/my_numbers.txt')
print(list(it))
print(list(it))  # Already exhausted


# ----------
it = read_visits('00_tmp/my_numbers.txt')

# 130
print(sum(it))

# 0
print(sum(it))


# ------------------------------------------------------------------------------
# copy the iterator as list inside function
# ------------------------------------------------------------------------------

def normalize_copy(numbers):
    numbers_copy = list(numbers)  # Copy the iterator as list
    total = sum(numbers_copy)
    result = []
    for value in numbers_copy:
        percent = 100 * value / total
        result.append(percent)
    return result


it = read_visits('00_tmp/my_numbers.txt')
num_copy = list(it)
percentages = normalize_copy(it)
print(percentages)
assert sum(percentages) == 100.0


# -->
# but this code has problem that 'numbers_copy' (list) would be very large and consumes memory ...


# ------------------------------------------------------------------------------
# pass iterator itself to function
# ------------------------------------------------------------------------------

# get_iter is:  lambda: read_visits(path), which returns generator
def normalize_func(get_iter):
    total = sum(get_iter())   # New iterator
    result = []
    for value in get_iter():  # New iterator
        percent = 100 * value / total
        result.append(percent)
    return result


path = '00_tmp/my_numbers.txt'
percentages = normalize_func(lambda: read_visits(path))
print(percentages)
assert sum(percentages) == 100.0


# ------------------------------------------------------------------------------
# Without lambda and 
# define new container class with iterator protocol
# ------------------------------------------------------------------------------

class ReadVisits:
    def __init__(self, data_path):
        self.data_path = data_path

    def __iter__(self):
        with open(self.data_path) as f:
            for line in f:
                yield int(line)


visits = ReadVisits(path)
percentages = normalize(visits)
print(percentages)
assert sum(percentages) == 100.0

# -->
# but this code read input data multiple times 


# ------------------------------------------------------------------------------
# Check whether input is container or iterator
# ------------------------------------------------------------------------------

def normalize_defensive(numbers):
    # ----------
    # if 'numbers' is iterator, iter(numbers) is also iterator.
    # if 'numbers' is container, iter(numbers) is iterator.
    if iter(numbers) is numbers:  # An iterator -- bad!
        raise TypeError('Must supply a container')
    # ----------
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

visits = [15, 35, 80]

normalize_defensive(visits)  # No error

# This raises error
normalize_defensive(iter(visits))


# ------------------------------------------------------------------------------
# Check whether input is container or iterator by collections.abc.Iterator
# ------------------------------------------------------------------------------

from collections.abc import Iterator 

def normalize_defensive(numbers):
    if isinstance(numbers, Iterator):  # Another way to check
        raise TypeError('Must supply a container')
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

visits = [15, 35, 80]

normalize_defensive(visits)  # No error

# This raises error
normalize_defensive(iter(visits))


# ------------------------------------------------------------------------------
# Now normalize_defensive works both for list and container class (with iterator protocol)
# ------------------------------------------------------------------------------

# list have iterator protocol
visits = [15, 35, 80]
percentages = normalize_defensive(visits)
assert sum(percentages) == 100.0

# visits is instance of container class with iterator protocol
visits = ReadVisits(path)
percentages = normalize_defensive(visits)
assert sum(percentages) == 100.0


# but does not work for iterator itself.
it = iter(visits)
percentages = normalize_defensive(it)
assert sum(percentages) == 100.0
