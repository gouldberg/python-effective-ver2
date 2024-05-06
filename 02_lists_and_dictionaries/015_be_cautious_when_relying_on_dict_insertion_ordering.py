#!/usr/bin/env PYTHONHASHSEED=1234 python3

from collections.abc import MutableMapping
from typing import Dict, MutableMapping, Iterator


# ------------------------------------------------------------------------------
# Python >= 3.6, order in dictionary is kept. (but NOT for Python <= 3.5)
# ------------------------------------------------------------------------------

baby_names = {
    'cat': 'kitten',
    'dog': 'puppy',
}

print(baby_names)


# ------------------------------------------------------------------------------
# check iteration order
# ------------------------------------------------------------------------------

print(list(baby_names.keys()))
print(list(baby_names.values()))
print(list(baby_names.items()))

# pop last item (random item for Python <= 3.5)
print(baby_names.popitem())


# ------------------------------------------------------------------------------
# **kwargs as dictionary
# this also keeps the order
# ------------------------------------------------------------------------------

# Note that **kwargs is dictionary inside the my_func. (kwargs.items())
def my_func(**kwargs):
    for key, value in kwargs.items():
        print(f'{key} = {value}')

my_func(goose='gosling', kangaroo='joey')


# ------------------------------------------------------------------------------
# class uses __dict__
# also keeps the order
# ------------------------------------------------------------------------------

class MyClass:
    def __init__(self):
        self.alligator = 'hatchling'
        self.elephant = 'calf'

a = MyClass()

for key, value in a.__dict__.items():
    print(f'{key} = {value}')


# ------------------------------------------------------------------------------
# example
# ------------------------------------------------------------------------------

def populate_ranks(votes, ranks):
    names = list(votes.keys())
    names.sort(key=votes.get, reverse=True)
    for i, name in enumerate(names, 1):
        ranks[name] = i

# next(iter(ranks)) return first key, irrespective of values
def get_winner(ranks):
    return next(iter(ranks))


votes = {
    'otter': 1281,
    'polar bear': 587,
    'fox': 863,
}

ranks = {}
# expected as otter --> fox --> polar bear (descending by values)
populate_ranks(votes, ranks)

# ranks is dictionary
type(ranks)
print(ranks)

# top one is winner !
winner = get_winner(ranks)
print(winner)


# ------------------------------------------------------------------------------
# use MutableMapping
# ------------------------------------------------------------------------------

class SortedDict(MutableMapping):
    def __init__(self):
        self.data = {}

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __iter__(self):
        # Now the ascending by key (name) not value
        keys = list(self.data.keys())
        keys.sort()
        for key in keys:
            yield key

    def __len__(self):
        return len(self.data)


# ----------
# just test for SortedDict()
my_dict = SortedDict()
my_dict['otter'] = 1
my_dict['cheeta'] = 2
my_dict['anteater'] = 3
my_dict['deer'] = 4
assert my_dict['otter'] == 1
assert 'cheeta' in my_dict
del my_dict['cheeta']
assert 'cheeta' not in my_dict
expected = [('anteater', 3), ('deer', 4), ('otter', 1)]
assert list(my_dict.items()) == expected
assert not isinstance(my_dict, dict)


# ----------
sorted_ranks = SortedDict()

populate_ranks(votes, sorted_ranks)

# not dictionary ..
type(sorted_ranks)

# not ascended by names ....
print(sorted_ranks.data)

# now __iter__ works and top is fox.
winner = get_winner(sorted_ranks)
print(winner)


# ------------------------------------------------------------------------------
# modify get_winner():  do not sue next(iter(ranks))
# ------------------------------------------------------------------------------

votes = {
    'otter': 1281,
    'polar bear': 587,
    'fox': 863,
}

ranks = {}
populate_ranks(votes, ranks)


# modify get_winner2, not use next(iter(ranks))
def get_winner2(ranks):
    for name, rank in ranks.items():
        if rank == 1:
            return name

# OK: expected as 'otter' 
winner = get_winner2(sorted_ranks)
print(winner)


# ------------------------------------------------------------------------------
# modify get_winner():  use next(iter(ranks) only for dictionary
# ------------------------------------------------------------------------------

# instance check
def get_winner3(ranks):
    if not isinstance(ranks, dict):
        raise TypeError('must provide a dict instance')
    return next(iter(ranks))

# OK
get_winner3(ranks) == 'otter'

# TypeError:  sorted_ranks is not dict instance.
get_winner3(sorted_ranks)


# ------------------------------------------------------------------------------
# Add type hints and checks by mypy.
# Check types in this file with:   python -m mypy --strict <path>
#  --> may produce 'Argument 2 to "populate_ranks" has incompatible type "SortedDict"; expected "Dict[str, int]'
#                  'Argument 1 to "get_winner" has incompatible type "SortedDict"; expected "Dict[str, int]'
# ------------------------------------------------------------------------------

def populate_ranks(votes: Dict[str, int],
                   ranks: Dict[str, int]) -> None:
    names = list(votes.keys())
    names.sort(key=votes.get, reverse=True)
    for i, name in enumerate(names, 1):
        ranks[name] = i


def get_winner(ranks: Dict[str, int]) -> str:
    return next(iter(ranks))


class SortedDict(MutableMapping[str, int]):
    def __init__(self) -> None:
        self.data: Dict[str, int] = {}

    def __getitem__(self, key: str) -> int:
        return self.data[key]

    def __setitem__(self, key: str, value: int) -> None:
        self.data[key] = value

    def __delitem__(self, key: str) -> None:
        del self.data[key]

    def __iter__(self) -> Iterator[str]:
        keys = list(self.data.keys())
        keys.sort()
        for key in keys:
            yield key

    def __len__(self) -> int:
        return len(self.data)

votes = {
    'otter': 1281,
    'polar bear': 587,
    'fox': 863,
}

sorted_ranks = SortedDict()
populate_ranks(votes, sorted_ranks)

print(sorted_ranks.data)

winner = get_winner(sorted_ranks)
print(winner)
