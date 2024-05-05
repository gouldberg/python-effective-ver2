#!/usr/bin/env PYTHONHASHSEED=1234 python3


# ------------------------------------------------------------------------------
# prepare texts
# ------------------------------------------------------------------------------

import random

fpath = '00_tmp/my_file.txt'

with open(fpath, 'w') as f:
    for _ in range(10):
        f.write('a' * random.randint(0, 100))
        f.write('\n')

value = [len(x) for x in open(fpath)]
print(value)


# ------------------------------------------------------------------------------
# generator
# ------------------------------------------------------------------------------

it = (len(x) for x in open(fpath))

#'it' is generator object
print(it)

print(next(it))
print(next(it))


# ------------------------------------------------------------------------------
# generator can be nested, and very fast
# ------------------------------------------------------------------------------

it = (len(x) for x in open(fpath))
value_it = list(it)


# generator nested
it = (len(x) for x in open(fpath))
roots = ((x, x**0.5) for x in it)
value_roots = list(roots)


print(value_it)
print(value_roots)
