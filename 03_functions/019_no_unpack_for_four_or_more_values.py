#!/usr/bin/env PYTHONHASHSEED=1234 python3


# ------------------------------------------------------------------------------
# get 2 unpacked values from return
# ------------------------------------------------------------------------------

def get_stats(numbers):
    minimum = min(numbers)
    maximum = max(numbers)
    return minimum, maximum

lengths = [63, 73, 72, 60, 67, 66, 71, 61, 72, 70]

minimum, maximum = get_stats(lengths)  # Two return values

print(f'Min: {minimum}, Max: {maximum}')


# ----------
first, second = 1, 2
assert first == 1
assert second == 2

def my_function():
    return 1, 2

first, second = my_function()
assert first == 1
assert second == 2


# ------------------------------------------------------------------------------
# catch-all unpack
# ------------------------------------------------------------------------------

def get_avg_ratio(numbers):
    average = sum(numbers) / len(numbers)
    scaled = [x / average for x in numbers]
    scaled.sort(reverse=True)
    return scaled

# *middle catches all except first and last
longest, *middle, shortest = get_avg_ratio(lengths)

# longest is 1.08148
# shortest is 0.88888
print(f'Longest:  {longest:>4.0%}')
print(f'Shortest: {shortest:>4.0%}')


# ------------------------------------------------------------------------------
# unpack 5 values
# ------------------------------------------------------------------------------

def get_stats(numbers):
    minimum = min(numbers)
    maximum = max(numbers)
    count = len(numbers)
    average = sum(numbers) / count

    sorted_numbers = sorted(numbers)
    middle = count // 2
    if count % 2 == 0:
        lower = sorted_numbers[middle - 1]
        upper = sorted_numbers[middle]
        median = (lower + upper) / 2
    else:
        median = sorted_numbers[middle]

    return minimum, maximum, average, median, count

minimum, maximum, average, median, count = get_stats(lengths)

print(f'Min: {minimum}, Max: {maximum}')
print(f'Average: {average}, Median: {median}, Count {count}')

assert minimum == 60
assert maximum == 73
assert average == 67.5
assert median == 68.5
assert count == 10


# Verify odd count median
_, _, _, median, count = get_stats([1, 2, 3])
assert median == 2
assert count == 3


# ------------------------------------------------------------------------------
# Unpack 4 or more values is not readable and easy to get bugged.
# ------------------------------------------------------------------------------

minimum, maximum, average, median, count = get_stats(
    lengths)

minimum, maximum, average, median, count = \
    get_stats(lengths)

(minimum, maximum, average,
 median, count) = get_stats(lengths)

(minimum, maximum, average, median, count
    ) = get_stats(lengths)
