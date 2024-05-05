#!/usr/bin/env PYTHONHASHSEED=1234 python3


# ------------------------------------------------------------------------------
# return None if exception is raised.
# Not only None but also other values (such as zero, empty) are also evaluated as False
# ------------------------------------------------------------------------------

def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None

assert careful_divide(4, 2) == 2
assert careful_divide(0, 1) == 0
assert careful_divide(3, 6) == 0.5
assert careful_divide(1, 0) == None


# ----------
x, y = 1, 0
result = careful_divide(x, y)

# result is None
print(result)

if result is None:
    print('Invalid inputs')
else:
    print('Result is %.1f' % result)


# ----------
x, y = 0, 5
result = careful_divide(x, y)

# result is not None but 0.0
print(result)

# result is 0.0  and 'if not result' will be True.
# Following statements are not correct.
if not result:
    print('Invalid inputs')  # This runs! But shouldn't
else:
    assert False


# ------------------------------------------------------------------------------
# return 2 values (computation success, and its result), but still result is None
# ------------------------------------------------------------------------------

def careful_divide(a, b):
    try:
        return True, a / b
    except ZeroDivisionError:
        return False, None

assert careful_divide(4, 2) == (True, 2)
assert careful_divide(0, 1) == (True, 0)
assert careful_divide(3, 6) == (True, 0.5)
assert careful_divide(1, 0) == (False, None)


# still result is None
x, y = 5, 0
_, result = careful_divide(x, y)
if not result:
    print('Invalid inputs')


# ------------------------------------------------------------------------------
# not return None, but convert ZeroDivisionError to raising ValueError
# type hint (return float) explicitly shows the function does not return None
# ------------------------------------------------------------------------------

def careful_divide(a: float, b: float) -> float:
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError('Invalid inputs')


x, y = 5, 2
x, y = 5, 0

try:
    result = careful_divide(x, y)
except ValueError:
    print('Invalid inputs')
else:
    print(f'Result is {result:.1f}')
