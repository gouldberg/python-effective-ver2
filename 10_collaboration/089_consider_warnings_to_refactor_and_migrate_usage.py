#!/usr/bin/env PYTHONHASHSEED=1234 python3

import warnings
import contextlib
import io
import logging


# ------------------------------------------------------------------------------
# unit conversion
# ------------------------------------------------------------------------------

def print_distance(speed, duration):
    distance = speed * duration
    print(f'{distance} miles')


# 5 miles/sec and 2.5 seconds are passed
# the unit of returned distance is mile
print_distance(5, 2.5)


# Someone passes not miles/sec but mistakenly meters/sec (1000 meters/sec)
print_distance(1000, 3)


# ----------
# now considering units conversion

CONVERSIONS = {
    'mph': 1.60934 / 3600 * 1000,   # m/s
    'hours': 3600,                  # seconds
    'miles': 1.60934 * 1000,        # m
    'meters': 1,                    # m
    'm/s': 1,                       # m
    'seconds': 1,                   # s
}

def convert(value, units):
    rate = CONVERSIONS[units]
    return rate * value


def localize(value, units):
    rate = CONVERSIONS[units]
    return value / rate


# Now the interface of print_distance is changed.
def print_distance(speed, duration, *,
                   speed_units='mph',
                   time_units='hours',
                   distance_units='miles'):
    norm_speed = convert(speed, speed_units)
    norm_duration = convert(duration, time_units)
    norm_distance = norm_speed * norm_duration
    distance = localize(norm_distance, distance_units)
    print(f'{distance} {distance_units}')


print_distance(1000, 3,
               speed_units='meters',
               time_units='seconds')


# ------------------------------------------------------------------------------
# use warnings.warn to notify for interface changing.
# speed_units, time_units, distance_units are all required to set.
# ------------------------------------------------------------------------------

def print_distance(speed, duration, *,
                   speed_units=None,
                   time_units=None,
                   distance_units=None):
    if speed_units is None:
        warnings.warn(
            'speed_units required', DeprecationWarning)
        speed_units = 'mph'

    if time_units is None:
        warnings.warn(
            'time_units required', DeprecationWarning)
        time_units = 'hours'

    if distance_units is None:
        warnings.warn(
            'distance_units required', DeprecationWarning)
        distance_units = 'miles'

    norm_speed = convert(speed, speed_units)
    norm_duration = convert(duration, time_units)
    norm_distance = norm_speed * norm_duration
    distance = localize(norm_distance, distance_units)
    print(f'{distance} {distance_units}')


fake_stderr = io.StringIO()

with contextlib.redirect_stderr(fake_stderr):
    print_distance(1000, 3,
                   speed_units='meters',
                   time_units='seconds')

print(fake_stderr.getvalue())


# ------------------------------------------------------------------------------
# stacklevel
# ------------------------------------------------------------------------------

def require(name, value, default):
    if value is not None:
        return value
    warnings.warn(
        f'{name} will be required soon, update your code',
        DeprecationWarning,
        stacklevel=3)
    return default


def print_distance(speed, duration, *,
                   speed_units=None,
                   time_units=None,
                   distance_units=None):
    speed_units = require('speed_units', speed_units, 'mph')
    time_units = require('time_units', time_units, 'hours')
    distance_units = require(
        'distance_units', distance_units, 'miles')

    norm_speed = convert(speed, speed_units)
    norm_duration = convert(duration, time_units)
    norm_distance = norm_speed * norm_duration
    distance = localize(norm_distance, distance_units)
    print(f'{distance} {distance_units}')


fake_stderr = io.StringIO()

with contextlib.redirect_stderr(fake_stderr):
    print_distance(1000, 3,
                   speed_units='meters',
                   time_units='seconds')

print(fake_stderr.getvalue())


# ------------------------------------------------------------------------------
# make all warnings to error to raise exception
# to be used:  'python3 -W error example_test.py'
# ------------------------------------------------------------------------------

warnings.simplefilter('error')

try:
    warnings.warn('This usage is deprecated',
                  DeprecationWarning)
except DeprecationWarning:
    pass  # Expected
else:
    assert False

warnings.resetwarnings()


# ------------------------------------------------------------------------------
# make all warnings to be ignored
# ------------------------------------------------------------------------------

warnings.resetwarnings()

warnings.simplefilter('ignore')

warnings.warn('This will not be printed to stderr')

warnings.resetwarnings()


# ------------------------------------------------------------------------------
# at production environment,
# copy warnings to logging
# ------------------------------------------------------------------------------

fake_stderr = io.StringIO()

handler = logging.StreamHandler(fake_stderr)

formatter = logging.Formatter(
    '%(asctime)-15s WARNING] %(message)s')

handler.setFormatter(formatter)

logging.captureWarnings(True)

logger = logging.getLogger('py.warnings')

logger.addHandler(handler)

logger.setLevel(logging.DEBUG)

warnings.resetwarnings()
warnings.simplefilter('default')
warnings.warn('This will go to the logs output')

print(fake_stderr.getvalue())

warnings.resetwarnings()


# ------------------------------------------------------------------------------
# unit test for warnings
# ------------------------------------------------------------------------------

# wrap require() defined above by warnings.catch_warnings as context manager.
with warnings.catch_warnings(record=True) as found_warnings:
    found = require('my_arg', None, 'fake units')
    expected = 'fake units'
    assert found == expected


assert len(found_warnings) == 1

single_warning = found_warnings[0]

assert str(single_warning.message) == (
    'my_arg will be required soon, update your code')

assert single_warning.category == DeprecationWarning
