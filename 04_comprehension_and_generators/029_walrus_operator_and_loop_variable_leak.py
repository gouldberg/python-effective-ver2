#!/usr/bin/env PYTHONHASHSEED=1234 python3

import logging

stock = {
    'nails': 125,
    'screws': 35,
    'wingnuts': 8,
    'washers': 24,
}

order = ['screws', 'wingnuts', 'clips']


# ------------------------------------------------------------------------------
# check inventory >= incoming order and incoming order >= minimum batch (=8)
# use 'for' 
# ------------------------------------------------------------------------------

def get_batches(count, size):
    return count // size

result = {}

for name in order:
  count = stock.get(name, 0)
  batches = get_batches(count, 8)
  if batches:
    result[name] = batches

print(result)


# ------------------------------------------------------------------------------
# use dict comprehension 
# ------------------------------------------------------------------------------

found = {name: get_batches(stock.get(name, 0), 8)
         for name in order
         if get_batches(stock.get(name, 0), 8)}

print(found)


# -->
# but since this program repeat twice same expression (get_batches(stock.get(name, 0), 8)),
# easy to be bugged as follows (now incorrectly 8 --> 4)

has_bug = {name: get_batches(stock.get(name, 0), 4)
           for name in order
           if get_batches(stock.get(name, 0), 8)}

print('Expected:', found)
print('Found:   ', has_bug)


# ------------------------------------------------------------------------------
# use walrus operator
# ------------------------------------------------------------------------------

found = {name: batches for name in order
         if (batches := get_batches(stock.get(name, 0), 8))}

assert found == {'screws': 4, 'wingnuts': 1}, found


# ------------------------------------------------------------------------------
# If the evaluation order is incorrect, this raise exception.
# ------------------------------------------------------------------------------

try:
    result = {name: (tenth := count // 10)
              for name, count in stock.items() if tenth > 0}
except:
    logging.exception('Expected')
else:
    assert False


# --> modified
result = {name: tenth for name, count in stock.items()
          if (tenth := count // 10) > 0}

print(result)


# ------------------------------------------------------------------------------
# loop variable leak
# ------------------------------------------------------------------------------

# loop variable in 'for' leaks
for count in stock.values():
    pass

# count is last item (=24)
print(f'Last item of {list(stock.values())} is {count}')


# ----------
# but list comprehension without assignment, no leaks.
half = [count // 2 for count in stock.values()]

# This raises NameError
print(f'Last item of {list(stock.values())} is {count}')


# ----------
# When you use walrus operator in comprehension, loop variable leaks too.
half = [(last := count // 2) for count in stock.values()]

print(f'Last item of {half} is {last}')


# ------------------------------------------------------------------------------
# walrus operator can be used in generators
# ------------------------------------------------------------------------------

found = ((name, batches) for name in order
         if (batches := get_batches(stock.get(name, 0), 8)))

print(next(found))
print(next(found))

