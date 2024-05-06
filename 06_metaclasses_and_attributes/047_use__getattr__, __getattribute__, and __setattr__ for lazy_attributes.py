#!/usr/bin/env PYTHONHASHSEED=1234 python3


# ------------------------------------------------------------------------------
# __getattr__
# If no attribute for its instance, __getattr_ is executed.
# ------------------------------------------------------------------------------

class LazyRecord:
    def __init__(self):
        self.exists = 5

    def __getattr__(self, name):
        value = f'Value for {name}'
        print('getter')
        setattr(self, name, value)
        return value


data = LazyRecord()

print('Before:', data.__dict__)


# ----------
# data instance does not have attribute 'foo',
# but since the instance have __getattr__ implemented,
# this is executed.
print('foo:   ', data.foo)


# ----------
# foo attribute is added.
# instance dictionary is updated.
print('After: ', data.__dict__)

# again getter, now do not print 'getter' message,
print('foo:   ', data.foo)


# ------------------------------------------------------------------------------
# __getattribute__
# Even if instance have given attribute, __getattribute_ is executed.
# ------------------------------------------------------------------------------

# add logging to LazyRecord
class LoggingLazyRecord(LazyRecord):
    def __getattr__(self, name):
        print(f'* Called __getattr__({name!r}), '
              f'populating instance dictionary')
        result = super().__getattr__(name)
        print(f'* Returning {result!r}')
        return result

data = LoggingLazyRecord()

print('exists:     ', data.exists)
print('First foo:  ', data.foo)
print('Second foo: ', data.foo)


# ----------
class ValidatingRecord:
    def __init__(self):
        self.exists = 5

    def __getattribute__(self, name):
        print(f'* Called __getattribute__({name!r})')
        try:
            value = super().__getattribute__(name)
            print(f'* Found {name!r}, returning {value!r}')
            return value
        except AttributeError:
            value = f'Value for {name}'
            print(f'* Setting {name!r} to {value!r}')
            setattr(self, name, value)
            return value


# ----------
data = ValidatingRecord()

# data instance have attribute 'exists', but still __getattribute__ is called.
# try block is executed
print('exists:     ', data.exists)

# data instance does not have attribute 'foo', __getattribute__ is called, too.
# else block is executed
print('First foo:  ', data.foo)

# 2nd time to get foo attribute,
# now, try block is executed
print('Second foo: ', data.foo)


# ------------------------------------------------------------------------------
# If some specific attribute SHOULD NOT be accessed,
# inside __getattr__ (or __getattribute__), define behavior for this case.
# ------------------------------------------------------------------------------

class MissingPropertyRecord:
    def __getattr__(self, name):
        if name == 'bad_name':
            raise AttributeError(f'{name} is missing')
        value = f'Value for {name}'
        setattr(self, name, value)
        return value

data = MissingPropertyRecord()

# works.
assert data.foo == 'Value for foo'  # Test this works

# this should not be accessed. --> AttributeError
data.bad_name


# ------------------------------------------------------------------------------
# hasattr:  check if instance have the specified attribute
# ------------------------------------------------------------------------------

data = LoggingLazyRecord()  # Implements __getattr__

print('Before:         ', data.__dict__)

# here __getattr__ is called
print('Has first foo:  ', hasattr(data, 'foo'))

print('After:          ', data.__dict__)
print('Has second foo: ', hasattr(data, 'foo'))


# ----------
data = ValidatingRecord()  # Implements __getattribute__

# here __getattribute__ is called
print('Has first foo:  ', hasattr(data, 'foo'))

# here also __getattribute__ is called
print('Has second foo: ', hasattr(data, 'foo'))


# ------------------------------------------------------------------------------
# setattr:  is called every time when set
# ------------------------------------------------------------------------------

class SavingRecord:
    def __setattr__(self, name, value):
        # Save some data for the record
        pass
        super().__setattr__(name, value)


class LoggingSavingRecord(SavingRecord):
    def __setattr__(self, name, value):
        print(f'* Called __setattr__({name!r}, {value!r})')
        super().__setattr__(name, value)


data = LoggingSavingRecord()
print('Before: ', data.__dict__)

# __setattr__ is called
data.foo = 5
print('After:  ', data.__dict__)

# __setattr__ is called
data.foo = 7
print('Finally:', data.__dict__)


# ------------------------------------------------------------------------------
# NOTE: if you do get inside __getattribute__,
# this will be recursion and produce RecursionError at stack limit.
# ------------------------------------------------------------------------------

class BrokenDictionaryRecord:
    def __init__(self, data):
        self._data = {}

    def __getattribute__(self, name):
        print(f'* Called __getattribute__({name!r})')
        # inside __getattribute__, getter here...(self._data)
        return self._data[name]


data = BrokenDictionaryRecord({'foo': 3})

# RecursionError.
data.foo


# ------------------------------------------------------------------------------
# use super().__getattribute__ of its instance to avoid recursion.
# ------------------------------------------------------------------------------

class DictionaryRecord:
    def __init__(self, data):
        self._data = data

    def __getattribute__(self, name):
        # Prevent weird interactions with isinstance() used
        # by example code harness.
        if name == '__class__':
            return DictionaryRecord
        print(f'* Called __getattribute__({name!r})')
        
        # use super().__getattribute__ of its instance to avoid recursion.
        data_dict = super().__getattribute__('_data')
        return data_dict[name]

data = DictionaryRecord({'foo': 3})

print('foo: ', data.foo)
