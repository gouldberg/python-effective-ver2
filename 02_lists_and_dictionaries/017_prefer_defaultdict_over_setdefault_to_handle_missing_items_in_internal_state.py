#!/usr/bin/env PYTHONHASHSEED=1234 python3

from collections import defaultdict


# ------------------------------------------------------------------------------
# setdefault() vs. get + walrus operator
# setdefault() is used regardless whether given key exists or not
# ------------------------------------------------------------------------------

visits = {
    'Mexico': {'Tulum', 'Puerto Vallarta'},
    'Japan': {'Hakone'},
}

# setdefault() is used regardless whether given key exists or not
visits.setdefault('Mexico', set()).add('Arles')  # Short
visits.setdefault('France', set()).add('Arles')  # Short
print(visits)


# get + walrus operator
if (japan := visits.get('Japan')) is None:       # Long
    visits['Japan'] = japan = set()

print(japan)

japan.add('Kyoto')
print(japan)

print(visits)


# ------------------------------------------------------------------------------
# wrap by class, use setdefault()
# ------------------------------------------------------------------------------

class Visits:
    def __init__(self):
        self.data = {}

    def add(self, country, city):
        # set required
        city_set = self.data.setdefault(country, set())
        city_set.add(city)


visits = Visits()
visits.add('Russia', 'Yekaterinburg')
visits.add('Tanzania', 'Zanzibar')

print(visits.data)


# ------------------------------------------------------------------------------
# wrap by class, use defaultdict(), more simple
# defaultdict() return default value if given key does not exist
#               when add, not required to set
# ------------------------------------------------------------------------------

class Visits:
    def __init__(self):
        self.data = defaultdict(set)

    def add(self, country, city):
        self.data[country].add(city)

visits = Visits()
visits.add('England', 'Bath')
visits.add('England', 'London')

print(visits.data)
