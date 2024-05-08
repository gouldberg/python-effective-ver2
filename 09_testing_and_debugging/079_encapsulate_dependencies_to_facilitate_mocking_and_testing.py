#!/usr/bin/env PYTHONHASHSEED=1234 python3

import contextlib
import io

from datetime import datetime
from datetime import timedelta
from unittest.mock import Mock
from unittest.mock import call
from unittest.mock import patch


# ------------------------------------------------------------------------------
# Encapsulate dependencies
# ------------------------------------------------------------------------------

class ZooDatabase:

    def get_animals(self, species):
        pass

    def get_food_period(self, species):
        pass

    def feed_animal(self, name, when):
        pass


# Create database class (ZooDatabase) and its mock instance
database = Mock(spec=ZooDatabase)

print(database.feed_animal)


# ----------
# Mock class instance can return mock object from Mock instance methods
database.feed_animal()

database.feed_animal.assert_any_call()


# ----------
# AttributeError
database.bad_method_name()


# ------------------------------------------------------------------------------
# Encapsulate dependencies and test
# ------------------------------------------------------------------------------

now_func = Mock(spec=datetime.utcnow)

now_func.return_value = datetime(2019, 6, 5, 15, 45)


# ----------
database = Mock(spec=ZooDatabase)

database.get_food_period.return_value = timedelta(hours=3)

database.get_animals.return_value = [
    ('Spot', datetime(2019, 6, 5, 11, 15)),
    ('Fluffy', datetime(2019, 6, 5, 12, 30)),
    ('Jojo', datetime(2019, 6, 5, 12, 55))
]


# ----------
def do_rounds(database, species, *, utcnow=datetime.utcnow):
    now = utcnow()
    feeding_timedelta = database.get_food_period(species)
    animals = database.get_animals(species)
    fed = 0

    for name, last_mealtime in animals:
        if (now - last_mealtime) >= feeding_timedelta:
            database.feed_animal(name, now)
            fed += 1

    return fed


# ----------
# do test
result = do_rounds(database, 'Meerkat', utcnow=now_func)

assert result == 2


# ----------
# check if method is called as expected
database.get_food_period.assert_called_once_with('Meerkat')

database.get_animals.assert_called_once_with('Meerkat')

database.feed_animal.assert_has_calls(
    [
        call('Spot', now_func.return_value),
        call('Fluffy', now_func.return_value),
    ],
    any_order=True)


# ------------------------------------------------------------------------------
# helper function for dependency injection
# global
# ------------------------------------------------------------------------------

# module scope
DATABASE = None

# helper function for dependency injection

def get_database():
    global DATABASE
    if DATABASE is None:
        DATABASE = ZooDatabase()
    return DATABASE


def main(argv):
    database = get_database()
    species = argv[1]
    count = do_rounds(database, species)
    print(f'Fed {count} {species}(s)')
    return 0


# ----------
with patch('__main__.DATABASE', spec=ZooDatabase):
    now = datetime.utcnow()

    DATABASE.get_food_period.return_value = timedelta(hours=3)
    DATABASE.get_animals.return_value = [
        ('Spot', now - timedelta(minutes=4.5)),
        ('Fluffy', now - timedelta(hours=3.25)),
        ('Jojo', now - timedelta(hours=3)),
    ]

    # 
    fake_stdout = io.StringIO()
    with contextlib.redirect_stdout(fake_stdout):
        main(['program name', 'Meerkat'])

    found = fake_stdout.getvalue()
    expected = 'Fed 2 Meerkat(s)\n'

    assert found == expected
