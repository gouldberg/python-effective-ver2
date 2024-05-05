#!/usr/bin/env PYTHONHASHSEED=1234 python3

import itertools

# ------------------------------------------------------------------------------
# itertools.chain
# itertools.repeat
# itertools.cycle
# itertools.tee
# ------------------------------------------------------------------------------

# ----------
# flatten, concatenate
it = itertools.chain([1, 2, 3], [4, 5, 6])
print(list(it))


# ----------
# repeat
it = itertools.repeat('hello', 3)
print(list(it))


# ----------
# cyclic repeat
it = itertools.cycle([1, 2])
result = [next(it) for _ in range (10)]
print(result)


# ----------
# parallel iterator
it1, it2, it3 = itertools.tee(['first', 'second'], 3)
print(list(it1))
print(list(it2))
print(list(it3))


# ------------------------------------------------------------------------------
# itertools.zip_longest
# ------------------------------------------------------------------------------

keys = ['one', 'two', 'three']
values = [1, 2]

normal = list(zip(keys, values))
print('zip:        ', normal)


# ----------
# zip (parallel) with longest sequence, fill value for shorters
it = itertools.zip_longest(keys, values, fillvalue='nope')
longest = list(it)
print('zip_longest:', longest)


# ------------------------------------------------------------------------------
# itertools.islice
# itertools.takewhile
# itertools.dropwhile
# itertools.filter / filterfalse
# itertools.accumulate
# ------------------------------------------------------------------------------

values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# ----------
# slice iterator
first_five = itertools.islice(values, 5)
print('First five: ', list(first_five))

# slice iterator by start, end, stride
middle_odds = itertools.islice(values, 2, 8, 2)
print('Middle odds:', list(middle_odds))


# ----------
# take while: take while func gets true (if false, end)
less_than_seven = lambda x: x < 7
it = itertools.takewhile(less_than_seven, values)
print(list(it))


# ----------
# drop while: skip while func gets false (if true, start)
less_than_seven = lambda x: x < 7
it = itertools.dropwhile(less_than_seven, values)
print(list(it))


# ----------
# filter / filterfalse
evens = lambda x: x % 2 == 0

filter_result = filter(evens, values)
print('Filter:      ', list(filter_result))

filter_false_result = itertools.filterfalse(evens, values)
print('Filter false:', list(filter_false_result))


# ----------
# accumulate
sum_reduce = itertools.accumulate(values)
print('Sum:   ', list(sum_reduce))

def sum_modulo_20(first, second):
    output = first + second
    return output % 20

# apply func
modulo_reduce = itertools.accumulate(values, sum_modulo_20)
print('Modulo:', list(modulo_reduce))


# ------------------------------------------------------------------------------
# itertools.product
# itertools.permutations
# itertools.combinations
# itertools.combinations_with_replacement
# ------------------------------------------------------------------------------

# ----------
# product: this case [(1,1),(1,2),(2,1),(2,2)]
single = itertools.product([1, 2], repeat=2)
print('Single:  ', list(single))


# ----------
# product: this case [(1,'a'),(1,'b'),(2,'a'),(2,'b')]
multiple = itertools.product([1, 2], ['a', 'b'])
print('Multiple:', list(multiple))


# ----------
# permutation
it = itertools.permutations([1, 2, 3, 4], 2)
print(list(it))


# combination
it = itertools.combinations([1, 2, 3, 4], 2)
print(list(it))


# combination with replacement
it = itertools.combinations_with_replacement([1, 2, 3, 4], 2)
print(list(it))
