#!/usr/bin/env PYTHONHASHSEED=1234 python3


# ------------------------------------------------------------------------------
# descriptor class 
# ------------------------------------------------------------------------------

# descriptor class
class Field:
    def __init__(self, name):
        self.name = name
        self.internal_name = '_' + self.name

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)


class Customer:
    # Class attributes
    first_name = Field('first_name')
    last_name = Field('last_name')
    prefix = Field('prefix')
    suffix = Field('suffix')


# ----------
cust = Customer()
print(f'Before: {cust.first_name!r} {cust.__dict__}')


# when set first name, cust.__dict__ is modified as expected.
cust.first_name = 'Euclid'
print(f'After:  {cust.first_name!r} {cust.__dict__}')


# ------------------------------------------------------------------------------
# use meta class 
# ------------------------------------------------------------------------------

# meta class
class Meta(type):
    def __new__(meta, name, bases, class_dict):
        for key, value in class_dict.items():
            if isinstance(value, Field):
                value.name = key
                value.internal_name = '_' + key
        cls = type.__new__(meta, name, bases, class_dict)
        return cls


# class to use meta class
class DatabaseRow(metaclass=Meta):
    pass


class Field:
    # constructor do NOT require name argument
    def __init__(self):
        # These will be assigned by the metaclass.
        self.name = None
        self.internal_name = None

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)


# class inherit DatabaseRow
# now you do not have to set arguments for Field()
class BetterCustomer(DatabaseRow):
    first_name = Field()
    last_name = Field()
    prefix = Field()
    suffix = Field()


cust = BetterCustomer()
print(f'Before: {cust.first_name!r} {cust.__dict__}')

cust.first_name = 'Euler'
print(f'After:  {cust.first_name!r} {cust.__dict__}')


# ------------------------------------------------------------------------------
# Do not forget inherit meta class
# ------------------------------------------------------------------------------

# If not inherit DatabaseRow
class BrokenCustomer:
    first_name = Field()
    last_name = Field()
    prefix = Field()
    suffix = Field()
    
cust = BrokenCustomer()

# TypeError
cust.first_name = 'Mersenne'


# ------------------------------------------------------------------------------
# use __set_name__ in descriptor
# Now not required to inherit meta class.
# descriptor checks data directly reduces the risk of memory leaks and weakref.
# ------------------------------------------------------------------------------

class Field:
    def __init__(self):
        self.name = None
        self.internal_name = None

    # use __set_name__:  check owner and attribute
    def __set_name__(self, owner, name):
        # Called on class creation for each descriptor
        self.name = name
        self.internal_name = '_' + name

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)


# Now not required to inherit meta class.
class FixedCustomer:
    first_name = Field()
    last_name = Field()
    prefix = Field()
    suffix = Field()


# ----------
cust = FixedCustomer()
print(f'Before: {cust.first_name!r} {cust.__dict__}')

cust.first_name = 'Mersenne'
print(f'After:  {cust.first_name!r} {cust.__dict__}')

