#!/usr/bin/env PYTHONHASHSEED=1234 python3

from time import sleep
from datetime import datetime


# ------------------------------------------------------------------------------
# datetime.now() set in keyword arguments is evaluated only once at definition
# ------------------------------------------------------------------------------

def log(message, when=datetime.now()):
    print(f'{when}: {message}')

log('Hi there!')


# time is not now ..., time stamp is same as above
# datetime.now is evaluated only once at log function is defined.
sleep(0.1)
log('Hello again!')


# ------------------------------------------------------------------------------
# set default None to keyword argument
# ------------------------------------------------------------------------------

def log(message, when=None):
    """Log a message with a timestamp.

    Args:
        message: Message to print.
        when: datetime of when the message occurred.
            Defaults to the present time.
    """
    if when is None:
        when = datetime.now()
    print(f'{when}: {message}')


log('Hi there!')

sleep(0.1)
log('Hello again!')


# ------------------------------------------------------------------------------
# set default None to keyword argument with type hint
# ------------------------------------------------------------------------------

from typing import Optional

def log_typed(message: str, when: Optional[datetime]=None) -> None:
    """Log a message with a timestamp.

    Args:
        message: Message to print.
        when: datetime of when the message occurred.
            Defaults to the present time.
    """
    if when is None:
        when = datetime.now()
    print(f'{when}: {message}')


log_typed('Hi there!')

sleep(0.1)
log_typed('Hello again!')




# ------------------------------------------------------------------------------
# default is shared by multiple instances !! 
# ------------------------------------------------------------------------------

import json

def decode(data, default={}):
    try:
        return json.loads(data)
    except ValueError:
        return default


foo = decode('bad data')
print(foo)


foo['stuff'] = 5
print(foo)


bar = decode('also bad')
# but this is same as foo
print(bar)


bar['meep'] = 1


# both of foo and bar has both of 'stuff' and 'meep'
print('Foo:', foo)
print('Bar:', bar)

assert foo is bar


# ------------------------------------------------------------------------------
# set default None to keyword argument
# ------------------------------------------------------------------------------

def decode(data, default=None):
    """Load JSON data from a string.

    Args:
        data: JSON data to decode.
        default: Value to return if decoding fails.
            Defaults to an empty dictionary.
    """
    try:
        return json.loads(data)
    except ValueError:
        if default is None:
            default = {}
        return default


foo = decode('bad data')
foo['stuff'] = 5

bar = decode('also bad')
bar['meep'] = 1

print('Foo:', foo)
print('Bar:', bar)

assert foo is not bar
