#!/usr/bin/env PYTHONHASHSEED=1234 python3


# ------------------------------------------------------------------------------
# zip : wrap 2 or more iterators 
# ------------------------------------------------------------------------------

names = ['Cecilia', 'Lise', 'Marie']

counts = [len(n) for n in names]

longest_name = None

max_count = 0

for name, count in zip(names, counts):
    if count > max_count:
        longest_name = name
        max_count = count

assert longest_name == 'Cecilia'


# ------------------------------------------------------------------------------
# zip ignores longer part of sequence (apply to shortest length)
# ------------------------------------------------------------------------------

names.append('Rosalind')

for name, count in zip(names, counts):
    print(name)


# ------------------------------------------------------------------------------
# itertools.zip_longest() apply to longest length
# ------------------------------------------------------------------------------

import itertools

for name, count in itertools.zip_longest(names, counts):
    print(f'{name}: {count}')


# --> For appended Rosalind, None for count.