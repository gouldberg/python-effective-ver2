#!/usr/bin/env PYTHONHASHSEED=1234 python3


# ------------------------------------------------------------------------------
# public attributes and private attributes
# ------------------------------------------------------------------------------

class MyObject:
    def __init__(self):
        self.public_field = 5
        # private attribute (double underscore '__' prefix)
        self.__private_field = 10

    def get_private_field(self):
        return self.__private_field


foo = MyObject()


# public attribute can be accessed by . operator
foo.public_field
assert foo.public_field == 5


# AttributeError
# private field can not be accessed.
foo.__private_field

# but is accessed via class method
assert foo.get_private_field() == 10


# ------------------------------------------------------------------------------
# class method can access to private attribute 
# ------------------------------------------------------------------------------

class MyOtherObject:
    def __init__(self):
        self.__private_field = 71

    @classmethod
    def get_private_field_of_instance(cls, instance):
        return instance.__private_field

bar = MyOtherObject()

# AttributeError
bar.__private_field

# but is accessed via class method
assert MyOtherObject.get_private_field_of_instance(bar) == 71


# ------------------------------------------------------------------------------
# subclass can not access to super class attribute
# but super class attribute can be accessed by super class attribute name
# ------------------------------------------------------------------------------

class MyParentObject:
    def __init__(self):
        self.__private_field = 71


class MyChildObject(MyParentObject):
    def get_private_field(self):
        return self.__private_field


baz = MyChildObject()

# AttributeError
# subclass can not access to super class attribute.
# NOTE: this error message shows '_MyChildObject__private_field' is the super class attribute name.
baz.get_private_field()

print(baz.__dict__)


# now use the super class attribute name
# this one can access to super class attribute
assert baz._MyParentObject__private_field == 71


# ------------------------------------------------------------------------------
# but access by super class attribute name is NOT robust !!
# ------------------------------------------------------------------------------

class MyStringClass:
    def __init__(self, value):
        self.__value = value

    def get_value(self):
        return str(self.__value)

foo = MyStringClass(5)

# AttributeError
foo.__value

# OK
assert foo.get_value() == '5'


# ----------
class MyIntegerSubclass(MyStringClass):
    def get_value(self):
        # here super class attribute name is used.
        return int(self._MyStringClass__value)

foo = MyIntegerSubclass('5')

# OK
assert foo.get_value() == 5


# ----------
# but access by super class attribute name is NOT robust !!

# now added MyBaseClass
class MyBaseClass:
    def __init__(self, value):
        self.__value = value

    def get_value(self):
        return self.__value

class MyStringClass(MyBaseClass):
    def get_value(self):
        return str(super().get_value())         # Updated

class MyIntegerSubclass(MyStringClass):
    def get_value(self):
        return int(self._MyStringClass__value)  # Not updated


foo = MyIntegerSubclass(5)

# AttributeError: 'MyIntegerSubclass' object has no attribute '_MyStringClass__value'
foo.get_value()


# ------------------------------------------------------------------------------
# This is better way.
#   add document (comments) in super class for future 
# ------------------------------------------------------------------------------

class MyStringClass:
    def __init__(self, value):
        # ----------------------------------------
        # THIS KIND OF COMMENT IS IMPORTANT
        # ----------------------------------------
        # This stores the user-supplied value for the object.
        # It should be coercible to a string. Once assigned in
        # the object it should be treated as immutable.
        self._value = value

    def get_value(self):
        return str(self._value)

class MyIntegerSubclass(MyStringClass):
    def get_value(self):
        return self._value

foo = MyIntegerSubclass(5)

assert foo.get_value() == 5


# ------------------------------------------------------------------------------
# Be careful attribute name conflicts
# ------------------------------------------------------------------------------

class ApiClass:
    def __init__(self):
        self._value = 5

    def get(self):
        return self._value


# If you define subclass while you do not know super class well.
class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello'  # Conflicts


a = Child()

print(f'{a.get()} and {a._value} should be different')


# ------------------------------------------------------------------------------
# Super class should use double underscore
# to avoid attribute name conflicts at inherited subclasses
# ------------------------------------------------------------------------------

class ApiClass:
    def __init__(self):
        self.__value = 5       # Double underscore

    def get(self):
        return self.__value    # Double underscore

class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello'  # OK!


a = Child()

print(f'{a.get()} and {a._value} are different')
