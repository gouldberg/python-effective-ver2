#!/usr/bin/env PYTHONHASHSEED=1234 python3

import logging


# ------------------------------------------------------------------------------
# raise ValueError
# ------------------------------------------------------------------------------

def determine_weight(volume, density):
    if density <= 0:
        raise ValueError('Density must be positive')


# ValueError: Density must be positive
determine_weight(1, 0)


# ------------------------------------------------------------------------------
# root Exception + try/else
# ------------------------------------------------------------------------------

class Error(Exception):
    """Base-class for all exceptions raised by this module."""


class InvalidDensityError(Error):
    """There was a problem with a provided density value."""


class InvalidVolumeError(Error):
    """There was a problem with the provided weight value."""


def determine_weight(volume, density):
    if density < 0:
        raise InvalidDensityError('Density must be positive')
    if volume < 0:
        raise InvalidVolumeError('Volume must be positive')
    if volume == 0:
        density / volume


class my_module:
    Error = Error
    InvalidDensityError = InvalidDensityError
    InvalidVolumeError = InvalidVolumeError

    @staticmethod
    def determine_weight(volume, density):
        if density < 0:
            raise InvalidDensityError('Density must be positive')
        if volume < 0:
            raise InvalidVolumeError('Volume must be positive')
        if volume == 0:
            density / volume


# ERROR:root:Unexpected error
# InvalidDensityError: Density must be positive
try:
    weight = my_module.determine_weight(1, -1)
except my_module.Error:
    logging.exception('Unexpected error')
else:
    assert False


# ----------
try:
    weight = my_module.determine_weight(1, -1)
except my_module.InvalidDensityError:
    weight = 0
except my_module.Error as e:
    logging.exception('Bug in the calling code')
else:
    assert False


# ------------------------------------------------------------------------------
# 
# ------------------------------------------------------------------------------

SENTINEL = object()

weight = SENTINEL

try:
    weight = my_module.determine_weight(0, 1)
except my_module.InvalidDensityError:
    weight = 0
except my_module.Error:
    logging.exception('Bug in the calling code')
else:
    assert False

assert weight is SENTINEL


# ------------------------------------------------------------------------------
# 
# ------------------------------------------------------------------------------

try:
    weight = SENTINEL
    try:
        weight = my_module.determine_weight(0, 1)
    except my_module.InvalidDensityError:
        weight = 0
    except my_module.Error:
        logging.exception('Bug in the calling code')
    except Exception:
        logging.exception('Bug in the API code!')
        raise  # Re-raise exception to the caller
    else:
        assert False
    
    assert weight == 0
except:
    logging.exception('Expected')
else:
    assert False


# ------------------------------------------------------------------------------
# 
# ------------------------------------------------------------------------------

class NegativeDensityError(InvalidDensityError):
    """A provided density value was negative."""


def determine_weight(volume, density):
    if density < 0:
        raise NegativeDensityError('Density must be positive')

try:
    my_module.NegativeDensityError = NegativeDensityError
    my_module.determine_weight = determine_weight
    try:
        weight = my_module.determine_weight(1, -1)
    except my_module.NegativeDensityError:
        raise ValueError('Must supply non-negative density')
    except my_module.InvalidDensityError:
        weight = 0
    except my_module.Error:
        logging.exception('Bug in the calling code')
    except Exception:
        logging.exception('Bug in the API code!')
        raise
    else:
        assert False
except:
    logging.exception('Expected')
else:
    assert False


# ------------------------------------------------------------------------------
# easier APIs extension by root Exception 
# ------------------------------------------------------------------------------

class Error(Exception):
    """Base-class for all exceptions raised by this module."""

class WeightError(Error):
    """Base-class for weight calculation errors."""

class VolumeError(Error):
    """Base-class for volume calculation errors."""

class DensityError(Error):
    """Base-class for density calculation errors."""

