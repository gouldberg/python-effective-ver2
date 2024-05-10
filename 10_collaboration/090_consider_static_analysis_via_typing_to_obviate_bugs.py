#!/usr/bin/env PYTHONHASHSEED=1234 python3

# This script is run by
# 'python3 -m mypy --strict <this script name>

from typing import Callable, List, TypeVar, Optional


# ------------------------------------------------------------------------------
# type of passed argument is NOT expected
# ------------------------------------------------------------------------------

def subtract(a: int, b: int) -> int:
    return a - b


# Oops: passed string value
subtract(10, '5')

# --> mypy says:
# Argument 2 to "subtract" has incompatible type "str"; expected "int" [arg-type]


# ------------------------------------------------------------------------------
# forgot self, return ...
# ------------------------------------------------------------------------------

class Counter:
    def __init__(self) -> None:
        # Field / variable annotation
        self.value: int = 0

    def add(self, offset: int) -> None:
        # Oops: forgot "self."
        # mypy says:
        # Name "value" is not defined [name-defined]
        value += offset

    # mypy says:
    # Missing return statement [return]
    def get(self) -> int:
        # Oops: forgot "return"
        self.value


counter = Counter()

counter.add(5)

counter.add(3)

assert counter.get() == 8


# ------------------------------------------------------------------------------
# add type hints by TypeVar and Callable to static analysis
# ------------------------------------------------------------------------------

# mypy says:
# Function is missing a type annotation [no-untyped-def]
def combine(func, values):
    assert len(values) > 0

    result = values[0]
    for next_value in values[1:]:
        result = func(result, next_value)

    return result


# mypy says:
# Function is missing a type annotation [no-untyped-def]
def add(x, y):
    return x + y


inputs = [1, 2, 3, 4j]

# mypy says:
# Call to untyped function "combine" in typed context [no-untyped-call]
result = combine(add, inputs)

# This fails
assert result == 10, result


# ----------
# add type hints by TypeVar and Callable to static analysis

Value = TypeVar('Value')

Func = Callable[[Value, Value], Value]

def combine2(func: Func[Value], values: List[Value]) -> Value:
    assert len(values) > 0

    result = values[0]
    for next_value in values[1:]:
        result = func(result, next_value)

    return result

Real = TypeVar('Real', int, float)

def add2(x: Real, y: Real) -> Real:
    return x + y


# Oops: included a complex number
inputs = [1, 2, 3, 4j]

# mypy says:
# Argument 1 to "combine2" has incompatible type "Callable[Real, Real], Real]"; expected "Callable[[complex. complex], complex]" [arg-type]
result = combine2(add2, inputs)

assert result == 10


# ------------------------------------------------------------------------------
# null check by Optional
# ------------------------------------------------------------------------------

def get_or_default(value: Optional[int],
                   default: int) -> int: 
    if value is not None:
        return value
    
    # mypy says:
    # Incompatible return value type (got "None", expected "int") [return-value]
    return value  # Oops: should have returned "default"


# ------------------------------------------------------------------------------
# A class is referencing to other class
# --> no check error by mypy
# --> type hint by string of class name
# ------------------------------------------------------------------------------

# FirstClass is referencing to other class
# This code does not produce error by mypy,
# but produce errors at runtime

class FirstClass:
    def __init__(self, value: SecondClass) -> None:
        self.value = value


class SecondClass:
    def __init__(self, value: int) -> None:
        self.value = value


second = SecondClass(5)

first = FirstClass(second)


# ----------
# Now type hint by string 'SecondClass'
class FirstClass:
    def __init__(self, value: 'SecondClass') -> None:
        self.value = value


class SecondClass:
    def __init__(self, value: int) -> None:
        self.value = value


second = SecondClass(5)

first = FirstClass(second)


# ------------------------------------------------------------------------------
# If you use, from __future__ import annotations,
# this ignores values specified at type hint completely at runtime,
# and resolve forward referencing.
# ------------------------------------------------------------------------------

from __future__ import annotations

class FirstClass:
    def __init__(self, value: SecondClass) -> None:
        self.value = value


class SecondClass:
    def __init__(self, value: int) -> None:
        self.value = value


second = SecondClass(5)

first = FirstClass(second)


