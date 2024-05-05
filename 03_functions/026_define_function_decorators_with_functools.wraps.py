#!/usr/bin/env PYTHONHASHSEED=1234 python3

from functools import wraps


# ------------------------------------------------------------------------------
# fibonacci function  (no decorated)
# ------------------------------------------------------------------------------

def fibonacci(n):
    """Return the n-th Fibonacci number"""
    if n in (0, 1):
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)

print(fibonacci(4))


# ------------------------------------------------------------------------------
# fibonacci function with wrapper
# ------------------------------------------------------------------------------

# get result(return of function) and print passed arguments
def trace(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f'{func.__name__}({args!r}, {kwargs!r}) '
              f'-> {result!r}')
        return result
    return wrapper

# wrapped fibonacci function
fibonacci = trace(fibonacci)

# output passed arguments and returned result each by stack level
fibonacci(4)


# ------------------------------------------------------------------------------
# fibonacci function (decorated by trace):  the output is same as above
# ------------------------------------------------------------------------------

@trace
def fibonacci(n):
    """Return the n-th Fibonacci number"""
    if n in (0, 1):
        return n
    return (fibonacci(n - 2) + fibonacci(n - 1))


fibonacci(4)

# but the function name is not fibonacci --> this is problem if you use introspection (such as at debugging)
# also pickle.dumps (object serializer) fails (if you try to do)
print(fibonacci)
help(fibonacci)


# ------------------------------------------------------------------------------
# use functools.wraps
# ------------------------------------------------------------------------------

def trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f'{func.__name__}({args!r}, {kwargs!r}) '
              f'-> {result!r}')
        return result
    return wrapper

@trace
def fibonacci(n):
    """Return the n-th Fibonacci number"""
    if n in (0, 1):
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)


# help works
# pickle.dumps(fibonacci) works (not shown here)
help(fibonacci)


