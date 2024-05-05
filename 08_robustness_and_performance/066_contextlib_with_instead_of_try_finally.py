#!/usr/bin/env PYTHONHASHSEED=1234 python3

from threading import Lock
import logging
from contextlib import contextmanager


# ------------------------------------------------------------------------------
# - with threading.lock
# - threading.lock.acquire --> try / finally lock.release()
# ------------------------------------------------------------------------------

lock = Lock()
with lock:
    # Do something while maintaining an invariant
    pass


# ----------
# above example is equivalent to:
lock.acquire()
try:
    # Do something while maintaining an invariant
    pass
finally:
    lock.release()


# ------------------------------------------------------------------------------
# use contextmanager decorator to change logger level
# ------------------------------------------------------------------------------

logging.getLogger().setLevel(logging.WARNING)

def my_function():
    logging.debug('Some debug data')
    logging.error('Error log here')
    logging.debug('More debug data')


# now logging level is WARNING --> only logging.error() is printed here.
my_function()


# ----------
# contextlib.contextmanager 

@contextmanager
def debug_logging(level):
    logger = logging.getLogger()
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield
    finally:
        logger.setLevel(old_level)


# with + decorated function:
# now the level is DEBUG, all logging message is printed
with debug_logging(logging.DEBUG):
    print('* Inside:')
    my_function()

# original:  only error level is shown
print('* After:')
my_function()


# ------------------------------------------------------------------------------
# use contextmanager decorator to change logger level
# ------------------------------------------------------------------------------

with open('00_tmp/my_output.txt', 'w') as handle:
    handle.write('This is some data!')


# yield logger
@contextmanager
def log_level(level, name):
    logger = logging.getLogger(name)
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        # yield logger here.
        yield logger
    finally:
        logger.setLevel(old_level)


logging.getLogger().setLevel(logging.WARNING)

# logging is warning level, so logging.debug() is not printed here.
with log_level(logging.DEBUG, 'my-log') as logger:
    logger.debug(f'This is a message for {logger.name}!')
    logging.debug('This will not print')


# now logger level is back to warning, logger.debug() is not printed here.
logger = logging.getLogger('my-log')
logger.debug('Debug will not print')
logger.error('Error will print')


# now logger is another instance.
with log_level(logging.DEBUG, 'other-log') as logger:
    logger.debug(f'This is a message for {logger.name}!')
    logging.debug('This will not print')
