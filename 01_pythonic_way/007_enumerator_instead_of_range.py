#!/usr/bin/env PYTHONHASHSEED=1234 python3

from random import randint


# ------------------------------------------------------------------------------
# generate random bits by range()
# ------------------------------------------------------------------------------

random_bits = 0

for i in range(32):
    if randint(0, 1):
        random_bits |= 1 << i

print(bin(random_bits))


# ------------------------------------------------------------------------------
# directly apply loop to sequence in list
# ------------------------------------------------------------------------------

flavor_list = ['vanilla', 'chocolate', 'pecan', 'strawberry']

for flavor in flavor_list:
    print(f'{flavor} is delicious')


# ------------------------------------------------------------------------------
# use range()
# ------------------------------------------------------------------------------

for i in range(len(flavor_list)):
    flavor = flavor_list[i]
    print(f'{i + 1}: {flavor}')


# ------------------------------------------------------------------------------
# enumerate() :  wrap iterator and yield loop index and next value
# ------------------------------------------------------------------------------

it = enumerate(flavor_list)

print(next(it))

print(next(it))


for i, flavor in enumerate(flavor_list):
    print(f'{i + 1}: {flavor}')


# ------------------------------------------------------------------------------
# unpack yielded by enumerate()
# ------------------------------------------------------------------------------

# default start index is 0
for i, flavor in enumerate(flavor_list):
    print(f'{i}: {flavor}')


# enumerate(, 1) start index from 1
for i, flavor in enumerate(flavor_list, 1):
    print(f'{i}: {flavor}')
