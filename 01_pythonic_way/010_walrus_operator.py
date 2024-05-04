#!/usr/bin/env PYTHONHASHSEED=1234 python3


# ------------------------------------------------------------------------------
# without walrus operator:
# get inventory --> by condition, print message
# ------------------------------------------------------------------------------

fresh_fruit = {
    'apple': 10,
    'banana': 8,
    'lemon': 5,
}

def make_lemonade(count):
    print(f'Making {count} lemons into lemonade')

def out_of_stock():
    print('Out of stock!')

count = fresh_fruit.get('lemon', 0)

if count:
    make_lemonade(count)
else:
    out_of_stock()


# -->
# When you read this code, newly created count variable is also required after this block...


# ------------------------------------------------------------------------------
# Use walrus operator:
# ------------------------------------------------------------------------------

# Explicitly shows that count variable is required only here.

if count := fresh_fruit.get('lemon', 0):
    make_lemonade(count)
else:
    out_of_stock()


# ------------------------------------------------------------------------------
# Use walrus operator
# and if with condition
# ------------------------------------------------------------------------------

def make_cider(count):
    print(f'Making cider with {count} apples')

if (count := fresh_fruit.get('apple', 0)) >= 4:
    make_cider(count)
else:
    out_of_stock()


# ------------------------------------------------------------------------------
# no walrus operator
# if condition --> try/except
# ------------------------------------------------------------------------------

def slice_bananas(count):
    print(f'Slicing {count} bananas')
    return count * 4

class OutOfBananas(Exception):
    pass

def make_smoothies(count):
    print(f'Making a smoothies with {count} banana slices')

# ----------
pieces = 0

count = fresh_fruit.get('banana', 0)

if count >= 2:
    pieces = slice_bananas(count)

try:
    smoothies = make_smoothies(pieces)
except OutOfBananas:
    out_of_stock()


# ------------------------------------------------------------------------------
# no walrus operator
# if condition + else --> try/except
# ------------------------------------------------------------------------------

count = fresh_fruit.get('banana', 0)

if count >= 2:
    pieces = slice_bananas(count)
else:
    # pieces = 0 in else block
    pieces = 0

try:
    smoothies = make_smoothies(pieces)
except OutOfBananas:
    out_of_stock()


# ------------------------------------------------------------------------------
# Use walrus operator
# if condition --> try/except
# ------------------------------------------------------------------------------

pieces = 0

if (count := fresh_fruit.get('banana', 0)) >= 2:
    pieces = slice_bananas(count)

try:
    smoothies = make_smoothies(pieces)
except OutOfBananas:
    out_of_stock()


# ------------------------------------------------------------------------------
# Use walrus operator
# if condition + else --> try/except
# ------------------------------------------------------------------------------

if (count := fresh_fruit.get('banana', 0)) >= 2:
    pieces = slice_bananas(count)
else:
    pieces = 0

try:
    smoothies = make_smoothies(pieces)
except OutOfBananas:
    out_of_stock()


# ------------------------------------------------------------------------------
# no walrus operator
# if else nested (python does not have switch/case expression)
# ------------------------------------------------------------------------------

count = fresh_fruit.get('banana', 0)

if count >= 2:
    pieces = slice_bananas(count)
    to_enjoy = make_smoothies(pieces)
else:
    count = fresh_fruit.get('apple', 0)
    if count >= 4:
        to_enjoy = make_cider(count)
    else:
        count = fresh_fruit.get('lemon', 0)
        if count:
            to_enjoy = make_lemonade(count)
        else:
            to_enjoy = 'Nothing'


# ------------------------------------------------------------------------------
# Use walrus operator
# if / elif (no nested, like switch/case expression)
# ------------------------------------------------------------------------------

if (count := fresh_fruit.get('banana', 0)) >= 2:
    pieces = slice_bananas(count)
    to_enjoy = make_smoothies(pieces)
elif (count := fresh_fruit.get('apple', 0)) >= 4:
    to_enjoy = make_cider(count)
elif count := fresh_fruit.get('lemon', 0):
    to_enjoy = make_lemonade(count)
else:
    to_enjoy = 'Nothing'


# ------------------------------------------------------------------------------
# no walrus operator, while loop
# ------------------------------------------------------------------------------

FRUIT_TO_PICK = [
    {'apple': 1, 'banana': 3},
    {'lemon': 2, 'lime': 5},
    {'orange': 3, 'melon': 2},
]

def pick_fruit():
    if FRUIT_TO_PICK:
        return FRUIT_TO_PICK.pop(0)
    else:
        return []

def make_juice(fruit, count):
    return [(fruit, count)]

bottles = []

fresh_fruit = pick_fruit()

while fresh_fruit:
    for fruit, count in fresh_fruit.items():
        batch = make_juice(fruit, count)
        bottles.extend(batch)
    fresh_fruit = pick_fruit()

print(bottles)


# ------------------------------------------------------------------------------
# no walrus operator, while loop + a half (if break)
# ------------------------------------------------------------------------------

FRUIT_TO_PICK = [
    {'apple': 1, 'banana': 3},
    {'lemon': 2, 'lime': 5},
    {'orange': 3, 'melon': 2},
]

bottles = []

while True:                     # Loop
    fresh_fruit = pick_fruit()
    if not fresh_fruit:         # And a half
        break
    for fruit, count in fresh_fruit.items():
        batch = make_juice(fruit, count)
        bottles.extend(batch)

print(bottles)


# ------------------------------------------------------------------------------
# walrus operator at while check condition
# ------------------------------------------------------------------------------

FRUIT_TO_PICK = [
    {'apple': 1, 'banana': 3},
    {'lemon': 2, 'lime': 5},
    {'orange': 3, 'melon': 2},
]

bottles = []

while fresh_fruit := pick_fruit():
    for fruit, count in fresh_fruit.items():
        batch = make_juice(fruit, count)
        bottles.extend(batch)

print(bottles)
