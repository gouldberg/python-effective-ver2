#!/usr/bin/env PYTHONHASHSEED=1234 python3


# ------------------------------------------------------------------------------
# No star (*) arguments
# You have to pass second argument
# ------------------------------------------------------------------------------

def log(message, values):
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print(f'{message}: {values_str}')

log('My numbers are', [1, 2])

# You have to pass second argument
log('Hi there', [])


# ------------------------------------------------------------------------------
# star (*) arguments 
# You do not have to pass second argument
# ------------------------------------------------------------------------------

def log2(message, *values):  # The only difference
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print(f'{message}: {values_str}')

log2('My numbers are', 1, 2)

# You do not have to pass second arguments
log2('Hi there')  # Much better


# ------------------------------------------------------------------------------
# star (*) arguments
# pass sequence to star argument
# ------------------------------------------------------------------------------

favorites = [7, 33, 99]

# This is OK
log('Favorite colors', favorites)

# This gives all 7, 33, 99 values independently
# --> TypeError: log() takes 2 positional arguments but 4 were given
log('Favorite colors', *favorites)

# This is OK
log2('Favorite colors', *favorites)


# ------------------------------------------------------------------------------
# star (*) arguments
# pass generator to star argument
# ------------------------------------------------------------------------------

def my_generator():
    for i in range(10):
        yield i

def my_func(*args):
    print(args)

it = my_generator()

my_func(*it)


# ------------------------------------------------------------------------------
# star (*) arguments
# ------------------------------------------------------------------------------

def log(sequence, message, *values):
    if not values:
        print(f'{sequence} - {message}')
    else:
        values_str = ', '.join(str(x) for x in values)
        print(f'{sequence} - {message}: {values_str}')

log(1, 'Favorites', 7, 33)      # New with *args OK

log(1, 'Hi there')              # New message only OK

log('Favorite numbers', 7, 33)  # Old usage breaks
