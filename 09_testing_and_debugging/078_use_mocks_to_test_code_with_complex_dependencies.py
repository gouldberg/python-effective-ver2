#!/usr/bin/env PYTHONHASHSEED=1234 python3

from datetime import datetime
from datetime import timedelta
from unittest.mock import Mock
from unittest.mock import ANY
from unittest.mock import call
from unittest.mock import patch
from unittest.mock import DEFAULT


# ------------------------------------------------------------------------------
# no mock
# ------------------------------------------------------------------------------

class DatabaseConnection:
    def __init__(self, host, port):
        pass

class DatabaseConnectionError(Exception):
    pass

def get_animals(database, species):
    # Query the Database
    raise DatabaseConnectionError('Not connected')
    # Return a list of (name, last_mealtime) tuples


database = DatabaseConnection('localhost', '4444')

get_animals(database, 'Meerkat')


# ------------------------------------------------------------------------------
# unittest.mock.Mock
# ------------------------------------------------------------------------------

# spec: mock is expected to behave as get_animals
# if this mock is used in different way, produce errors.
mock = Mock(spec=get_animals)

mock

expected = [
    ('Spot', datetime(2019, 6, 5, 11, 15)),
    ('Fluffy', datetime(2019, 6, 5, 12, 30)),
    ('Jojo', datetime(2019, 6, 5, 12, 45)),
]

# when called, return this value
mock.return_value = expected

# if access to attributes which does not exists in mock,
# produce AttributeError.
mock.does_not_exist


# ----------
database = object()

# now this mock returns expected values
result = mock(database, 'Meerkat')

assert result == expected


# ------------------------------------------------------------------------------
# unittest.mock.Mock
# check whether the function calling this mock specified correct arguments
# ------------------------------------------------------------------------------

# now function get_animals is called by 'Meerkat'
mock.assert_called_once_with(database, 'Meerkat')


# this raises exceptions
mock.assert_called_once_with(database, 'Giraffe')


# ----------
mock = Mock(spec=get_animals)

mock('database 1', 'Rabbit')

# OK
mock.assert_called_once_with('database 1', 'Rabbit')


# ----------
mock = Mock(spec=get_animals)

mock('database 2', 'Bison')

# AssertionError: expected call not found
mock.assert_called_once_with('database 1', 'Rabbit')

# AssertionError: expected call not found
mock.assert_called_once_with('database 1', 'Bison')

# OK
mock.assert_called_once_with('database 2', 'Bison')


# ----------
mock = Mock(spec=get_animals)

mock('database 2', 'Bison')
mock('database 3', 'Meerkat')

# AssertionError:  Expected 'mock' to be called once, Called 2 times.
mock.assert_called_once_with('database 2', 'Bison')


# ------------------------------------------------------------------------------
# unittest.mock.Mock
# assert_called_with(ANY, ):  ANY can represent any arguments
# ------------------------------------------------------------------------------

mock = Mock(spec=get_animals)

mock('database 2', 'Bison')
mock('database 3', 'Meerkat')

# OK
mock.assert_called_with(ANY, 'Meerkat')

# AssertionError
mock.assert_called_with(ANY, 'Rabbit')


# ------------------------------------------------------------------------------
# unittest.mock.Mock
# raise exception by mock:  set at side_effect
# ------------------------------------------------------------------------------

class MyError(Exception):
    pass

mock = Mock(spec=get_animals)

mock.side_effect = MyError('Whoops! Big problem')

result = mock(database, 'Meerkat')


# ------------------------------------------------------------------------------
# some original program
# ------------------------------------------------------------------------------

def get_food_period(database, species):
    # Query the Database
    pass
    # Return a time delta


def feed_animal(database, name, when):
    # Write to the Database
    pass


def do_rounds(database, species):
    now = datetime.datetime.utcnow()
    feeding_timedelta = get_food_period(database, species)
    animals = get_animals(database, species)
    fed = 0

    for name, last_mealtime in animals:
        if (now - last_mealtime) > feeding_timedelta:
            feed_animal(database, name, now)
            fed += 1

    return fed


# ------------------------------------------------------------------------------
# test
# ------------------------------------------------------------------------------

def do_rounds(database, species, *,
              now_func=datetime.utcnow,
              food_func=get_food_period,
              animals_func=get_animals,
              feed_func=feed_animal):
    now = now_func()
    feeding_timedelta = food_func(database, species)
    animals = animals_func(database, species)
    fed = 0

    for name, last_mealtime in animals:
        if (now - last_mealtime) > feeding_timedelta:
            feed_func(database, name, now)
            fed += 1

    return fed


# -----------
# set mock to datetime.utcnow
now_func = Mock(spec=datetime.utcnow)
now_func.return_value = datetime(2019, 6, 5, 15, 45)


# -----------
# set mock to get_food_period
food_func = Mock(spec=get_food_period)
food_func.return_value = timedelta(hours=3)


# -----------
# set mock to get_animals
animals_func = Mock(spec=get_animals)

animals_func.return_value = [
    ('Spot', datetime(2019, 6, 5, 11, 15)),
    ('Fluffy', datetime(2019, 6, 5, 12, 30)),
    ('Jojo', datetime(2019, 6, 5, 12, 45)),
]


# -----------
# set mock to feed_animal
feed_func = Mock(spec=feed_animal)


# -----------
# check the result
# pass mock and override default argument value

result = do_rounds(
    database,
    'Meerkat',
    now_func=now_func,
    food_func=food_func,
    animals_func=animals_func,
    feed_func=feed_func)

assert result == 2


# -----------
# both functions are called once by (database, 'Meerkat')
food_func.assert_called_once_with(database, 'Meerkat')

animals_func.assert_called_once_with(database, 'Meerkat')


# ------------------------------------------------------------------------------
# test
# check a function calling other functions
# ------------------------------------------------------------------------------

# check feed_func calls now_func 2 times (do not care for calling order)
feed_func.assert_has_calls(
    [
        call(database, 'Spot', now_func.return_value),
        call(database, 'Fluffy', now_func.return_value),
    ],
    any_order=True)


# ------------------------------------------------------------------------------
# test
# use patch to override function
# ------------------------------------------------------------------------------

print('Outside patch:', get_animals)

with patch('__main__.get_animals'):
    print('Inside patch: ', get_animals)

print('Outside again:', get_animals)


# ----------
# but datetime is defined by C extension module, patch can not be applied in same way
fake_now = datetime(2019, 6, 5, 15, 45)
    
with patch('datetime.datetime.utcnow'):
    datetime.utcnow.return_value = fake_now


# ----------
# define helper function to return datetime.datetime.utcnow()
def get_do_rounds_time():
    return datetime.datetime.utcnow()

def do_rounds(database, species):
    now = get_do_rounds_time()

with patch('__main__.get_do_rounds_time'):
    pass


# ----------
# or
#   use keyword arguments for datetime.utcnow mock
#   use patch for other mocks
def do_rounds(database, species, *, utcnow=datetime.utcnow):
    now = utcnow()
    feeding_timedelta = get_food_period(database, species)
    animals = get_animals(database, species)
    fed = 0

    for name, last_mealtime in animals:
        if (now - last_mealtime) > feeding_timedelta:
            feed_animal(database, name, now)
            fed += 1

    return fed


# ------------------------------------------------------------------------------
# with patch.multiple
# ------------------------------------------------------------------------------

with patch.multiple('__main__',
                    autospec=True,
                    get_food_period=DEFAULT,
                    get_animals=DEFAULT,
                    feed_animal=DEFAULT):
    now_func = Mock(spec=datetime.utcnow)
    now_func.return_value = datetime(2019, 6, 5, 15, 45)
    get_food_period.return_value = timedelta(hours=3)
    get_animals.return_value = [
        ('Spot', datetime(2019, 6, 5, 11, 15)),
        ('Fluffy', datetime(2019, 6, 5, 12, 30)),
        ('Jojo', datetime(2019, 6, 5, 12, 45))
    ]

    # utcnow for keyword argument
    result = do_rounds(database, 'Meerkat', utcnow=now_func)
    assert result == 2

    get_food_period.assert_called_once_with(database, 'Meerkat')
    get_animals.assert_called_once_with(database, 'Meerkat')
    feed_animal.assert_has_calls(
        [
            call(database, 'Spot', now_func.return_value),
            call(database, 'Fluffy', now_func.return_value),
        ],
        any_order=True)
