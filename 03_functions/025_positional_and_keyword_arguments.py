#!/usr/bin/env PYTHONHASHSEED=1234 python3

# ------------------------------------------------------------------------------
# 2 boolean in positional arguments
# --> this may confuse ...
# ------------------------------------------------------------------------------

def safe_division(number, divisor,
                  ignore_overflow,
                  ignore_zero_division):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

# 2 boolean in positional arguments
result = safe_division(1.0, 10**500, True, False)
print(result)


# 2 boolean in positional arguments
result = safe_division(1.0, 0, False, True)
print(result)


# ------------------------------------------------------------------------------
# Changed to keyword arguments and set default
# ------------------------------------------------------------------------------

def safe_division_b(number, divisor,
                    ignore_overflow=False,        # Changed
                    ignore_zero_division=False):  # Changed
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise


result = safe_division_b(1.0, 10**500, ignore_overflow=True)
print(result)

result = safe_division_b(1.0, 0, ignore_zero_division=True)
print(result)


assert safe_division_b(1.0, 10**500, True, False) == 0


# ------------------------------------------------------------------------------
# * means end of positional arguments and start of keyword arguments
# ------------------------------------------------------------------------------

def safe_division_c(number, divisor, *,  # Changed
                    ignore_overflow=False,
                    ignore_zero_division=False):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise


# This will produce TypeError: safe_division_c() takes 2 positional arguments but 4 were given
safe_division_c(1.0, 10**500, True, False)

# This works
result = safe_division_c(1.0, 0, ignore_zero_division=True)
assert result == float('inf')

# ZeroDivisionError
result = safe_division_c(1.0, 0)


assert safe_division_c(number=2, divisor=5) == 0.4
assert safe_division_c(divisor=5, number=2) == 0.4
assert safe_division_c(2, divisor=5) == 0.4


# ------------------------------------------------------------------------------
# changed arguments name of positional arguments
# ------------------------------------------------------------------------------

def safe_division_c(numerator, denominator, *,  # Changed
                    ignore_overflow=False,
                    ignore_zero_division=False):
    try:
        return numerator / denominator
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

# This is TypeError
safe_division_c(number=2, divisor=5)


# ------------------------------------------------------------------------------
# '/' means end of positional arguments
# ------------------------------------------------------------------------------

def safe_division_d(numerator, denominator, /, *,  # Changed
                    ignore_overflow=False,
                    ignore_zero_division=False):
    try:
        return numerator / denominator
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

# positional arguments:  This works
assert safe_division_d(2, 5) == 0.4

# use keyword arguments:  Type Error
safe_division_d(numerator=2, denominator=5)


# ------------------------------------------------------------------------------
# arguments placed between '/' and '*'
# are positional OR keyword (both are applicable !!)
# ------------------------------------------------------------------------------

def safe_division_e(numerator, denominator, /,
                    ndigits=10, *,                # Changed
                    ignore_overflow=False,
                    ignore_zero_division=False):
    try:
        fraction = numerator / denominator        # Changed
        return round(fraction, ndigits)           # Changed
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

# Followings all works.

# ndigits is keyword argument (defualt is applied)
result = safe_division_e(22, 7)
print(result)

# ndigits is positional argument
result = safe_division_e(22, 7, 5)
print(result)

# ndigits is keyword argument
result = safe_division_e(22, 7, ndigits=2)
print(result)