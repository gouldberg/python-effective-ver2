#!/usr/bin/env PYTHONHASHSEED=1234 python3


# ------------------------------------------------------------------------------
# dictionary to tuple 
# ------------------------------------------------------------------------------

snack_calories = {
    'chips': 140,
    'popcorn': 80,
    'nuts': 190,
}

items = tuple(snack_calories.items())

print(items)


# ------------------------------------------------------------------------------
# access to tuple value by index
# ------------------------------------------------------------------------------

item = ('Peanut butter', 'Jelly')

first = item[0]

second = item[1]

print(first, 'and', second)


# ------------------------------------------------------------------------------
# cannot substitute(assignment) to tuple by index
# ------------------------------------------------------------------------------

pair = ('Chocolate', 'Peanut butter')

# Type Error
pair[0] = 'Honey'


# ------------------------------------------------------------------------------
# unpack
# ------------------------------------------------------------------------------

item = ('Peanut butter', 'Jelly')

first, second = item  # Unpacking

print(first, 'and', second)


# ------------------------------------------------------------------------------
# Unpack to deep level
# ------------------------------------------------------------------------------

favorite_snacks = {
    'salty': ('pretzels', 100),
    'sweet': ('cookies', 180),
    'veggie': ('carrots', 20),
}

((type1, (name1, cals1)),
 (type2, (name2, cals2)),
 (type3, (name3, cals3))) = favorite_snacks.items()

print(f'Favorite {type1} is {name1} with {cals1} calories')
print(f'Favorite {type2} is {name2} with {cals2} calories')
print(f'Favorite {type3} is {name3} with {cals3} calories')


# ------------------------------------------------------------------------------
# bubble sort:  naive way
# ------------------------------------------------------------------------------

def bubble_sort(a):
    for _ in range(len(a)):
        for i in range(1, len(a)):
            if a[i] < a[i-1]:
                temp = a[i]
                a[i] = a[i-1]
                a[i-1] = temp

names = ['pretzels', 'carrots', 'arugula', 'bacon']

bubble_sort(names)

print(names)


# ------------------------------------------------------------------------------
# bubble sort:  use swap
# ------------------------------------------------------------------------------

def bubble_sort(a):
    for _ in range(len(a)):
        for i in range(1, len(a)):
            if a[i] < a[i-1]:
                a[i-1], a[i] = a[i], a[i-1]  # Swap

names = ['pretzels', 'carrots', 'arugula', 'bacon']

bubble_sort(names)

print(names)


# ------------------------------------------------------------------------------
# use unpack in enumerate()
# ------------------------------------------------------------------------------

snacks = [('bacon', 350), ('donut', 240), ('muffin', 190)]

for i in range(len(snacks)):
    item = snacks[i]
    name = item[0]
    calories = item[1]
    print(f'#{i+1}: {name} has {calories} calories')


for rank, (name, calories) in enumerate(snacks):
    print(f'#{rank}: {name} has {calories} calories')

