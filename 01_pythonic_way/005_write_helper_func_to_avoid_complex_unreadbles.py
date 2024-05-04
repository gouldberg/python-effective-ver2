#!/usr/bin/env PYTHONHASHSEED=1234 python3

from urllib.parse import parse_qs

# ------------------------------------------------------------------------------
# get value for key from dictionary
# ------------------------------------------------------------------------------

query_string = 'red=5&blue=0&green='

my_values = parse_qs(query_string,
                     keep_blank_values=True)

print(my_values)
print(repr(my_values))


# get value for each key
print('Red:     ', my_values.get('red'))
print('Green:   ', my_values.get('green'))
print('Opacity: ', my_values.get('opacity'))


# ------------------------------------------------------------------------------
# replace empty list, None by 0
# ------------------------------------------------------------------------------

# if [''], replace by 0
# In Python, empty string, empty list, zero is evaluated as False

red = my_values.get('red', [''])[0] or 0
green = my_values.get('green', [''])[0] or 0
opacity = my_values.get('opacity', [''])[0] or 0

print(f'Red:     {red!r}')
print(f'Green:   {green!r}')
print(f'Opacity: {opacity!r}')


# ------------------------------------------------------------------------------
# wrap by int() to convert to int 
# ------------------------------------------------------------------------------

red = int(my_values.get('red', [''])[0] or 0)
green = int(my_values.get('green', [''])[0] or 0)
opacity = int(my_values.get('opacity', [''])[0] or 0)

print(f'Red:     {red!r}')
print(f'Green:   {green!r}')
print(f'Opacity: {opacity!r}')

# --> not readable ...


# ------------------------------------------------------------------------------
# RECOMMENDED: 
# use ternary expression: x if condition else y
# ------------------------------------------------------------------------------

red_str = my_values.get('red', [''])
red = int(red_str[0]) if red_str[0] else 0

green_str = my_values.get('green', [''])
green = int(green_str[0]) if green_str[0] else 0

opacity_str = my_values.get('opacity', [''])
opacity = int(opacity_str[0]) if opacity_str[0] else 0

print(f'Red:     {red!r}')
print(f'Green:   {green!r}')
print(f'Opacity: {opacity!r}')


# ------------------------------------------------------------------------------
# write helper function
# ------------------------------------------------------------------------------

def get_first_int(values, key, default=0):
    found = values.get(key, [''])
    if found[0]:
        return int(found[0])
    return default


green = get_first_int(my_values, 'green')
red = get_first_int(my_values, 'red')
opacity = get_first_int(my_values, 'opacity')

print(f'Red:     {red!r}')
print(f'Green:   {green!r}')
print(f'Opacity: {opacity!r}')
