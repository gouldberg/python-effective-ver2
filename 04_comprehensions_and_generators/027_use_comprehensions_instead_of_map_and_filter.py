#!/usr/bin/env PYTHONHASHSEED=1234 python3


a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


# ------------------------------------------------------------------------------
# map + filter version
# ------------------------------------------------------------------------------

# map
alt = map(lambda x: x ** 2, a)
print(f'alt : {alt}')


# map + filter
alt = map(lambda x: x**2, filter(lambda x: x % 2 == 0, a))
print(f'alt : {alt}')


alt_dict = dict(map(lambda x: (x, x**2), filter(lambda x: x % 2 == 0, a)))
alt_set = set(map(lambda x: x**3, filter(lambda x: x % 3 == 0, a)))
print(f'alt_dict : {alt_dict}')
print(f'alt_set : {alt_set}')


# ------------------------------------------------------------------------------
# list / dict / set comprehension
# ------------------------------------------------------------------------------

# list comprehension
even_squares = [x**2 for x in a if x % 2 == 0]
print(f'even_squares : {even_squares}')


# dict, set comprehension
even_squares_dict = {x: x**2 for x in a if x % 2 == 0}
threes_cubed_set = {x**3 for x in a if x % 3 == 0}
print(f'even_squares_dict : {even_squares_dict}')
print(f'threes_cubed_set : {threes_cubed_set}')
