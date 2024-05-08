#!/usr/bin/env PYTHONHASHSEED=1234 python3

from functools import wraps
import types


# ------------------------------------------------------------------------------
# debug decorator
# to output arguments, returns and exceptions for all methods
# ------------------------------------------------------------------------------

def trace_func(func):
    if hasattr(func, 'tracing'):  # Only decorate once
        return func

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            result = e
            raise
        finally:
            print(f'{func.__name__}({args!r}, {kwargs!r}) -> '
                  f'{result!r}')

    wrapper.tracing = True
    return wrapper


# apply debug decorate defined above to dict subclasses
class TraceDict(dict):
    @trace_func
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @trace_func
    def __setitem__(self, *args, **kwargs):
        return super().__setitem__(*args, **kwargs)

    @trace_func
    def __getitem__(self, *args, **kwargs):
        return super().__getitem__(*args, **kwargs)


# ----------
trace_dict = TraceDict([('hi', 1)])

trace_dict['there'] = 2

trace_dict['hi']

# KeyError
trace_dict['does not exist']


# ------------------------------------------------------------------------------
# decorate automatically class methods by using meta class
# ------------------------------------------------------------------------------

trace_types = (
    types.MethodType,
    types.FunctionType,
    types.BuiltinFunctionType,
    types.BuiltinMethodType,
    types.MethodDescriptorType,
    types.ClassMethodDescriptorType)


class TraceMeta(type):
    def __new__(meta, name, bases, class_dict):
        klass = super().__new__(meta, name, bases, class_dict)

        for key in dir(klass):
            value = getattr(klass, key)
            if isinstance(value, trace_types):
                
                # trace_func decorator
                wrapped = trace_func(value)
                setattr(klass, key, wrapped)

        return klass


class TraceDict(dict, metaclass=TraceMeta):
    pass

trace_dict = TraceDict([('hi', 1)])

trace_dict['there'] = 2

trace_dict['hi']

# KeyError
trace_dict['does not exist']


# ------------------------------------------------------------------------------
# meta class inheritance
# ------------------------------------------------------------------------------

trace_types = (
    types.MethodType,
    types.FunctionType,
    types.BuiltinFunctionType,
    types.BuiltinMethodType,
    types.MethodDescriptorType,
    types.ClassMethodDescriptorType)


class OtherMeta(type):
    pass


# this class has has meta class
class SimpleDict(dict, metaclass=OtherMeta):
    pass


# TraceMeta does not inherit OtherMeta
# TypeError: metaclass conflict
class TraceDict(SimpleDict, metaclass=TraceMeta):
    pass


# ----------
# now TraceMeta inherit OtherMeta (meta class inheritance)
class TraceMeta(type):
    def __new__(meta, name, bases, class_dict):
        # now NOT super().__new__ but type.__new__
        klass = type.__new__(meta, name, bases, class_dict)

        for key in dir(klass):
            value = getattr(klass, key)
            if isinstance(value, trace_types):
                
                # trace_func decorator
                wrapped = trace_func(value)
                setattr(klass, key, wrapped)

        return klass


class OtherMeta(TraceMeta):
    pass

class SimpleDict(dict, metaclass=OtherMeta):
    pass

class TraceDict(SimpleDict, metaclass=TraceMeta):
    pass


# ----------
trace_dict = TraceDict([('hi', 1)])

trace_dict['there'] = 2

trace_dict['hi']

trace_dict['does not exist']


# ------------------------------------------------------------------------------
# Not using meta class...
# But use class decorator
# class decorator takes class instance as argument.
# returns new class or modified version of original class
# ------------------------------------------------------------------------------

# class decorator takes class instance as argument.
# returns new class or modified version of original class
def trace(klass):
    for key in dir(klass):
        value = getattr(klass, key)
        if isinstance(value, trace_types):
            # trace_func itself is decorator
            wrapped = trace_func(value)
            setattr(klass, key, wrapped)
    return klass


@trace
class TraceDict(dict):
    pass


trace_dict = TraceDict([('hi', 1)])

trace_dict['there'] = 2

trace_dict['hi']

# KeyError
trace_dict['does not exist']


# ------------------------------------------------------------------------------
# class decorator @trace works also for meta class is already defined. 
# ------------------------------------------------------------------------------

class OtherMeta(type):
    pass


# class decorator @trace works also for meta class is already defined. 
@trace
class TraceDict(dict, metaclass=OtherMeta):
    pass


trace_dict = TraceDict([('hi', 1)])

trace_dict['there'] = 2

trace_dict['hi']

trace_dict['does not exist']
