#!/usr/bin/env PYTHONHASHSEED=1234 python3


# ------------------------------------------------------------------------------
# initialize super class from subclass
# ------------------------------------------------------------------------------

class MyBaseClass:
    def __init__(self, value):
        self.value = value

class MyChildClass(MyBaseClass):
    def __init__(self):
        # initialize super class from subclass
        MyBaseClass.__init__(self, 5)

    def times_two(self):
        return self.value * 2

foo = MyChildClass()

assert foo.times_two() == 10


#   --> not good way (not expected in multiple inheritance)
#       the order of calling __init__ method is not pre-defined for all subclasses


# ------------------------------------------------------------------------------
# initialize super class from subclass:  multiple inheritance and multiple initialization
# ------------------------------------------------------------------------------

class TimesTwo:
    def __init__(self):
        self.value *= 2

class PlusFive:
    def __init__(self):
        self.value += 5

# multiple inheritance and multiple initialization
class OneWay(MyBaseClass, TimesTwo, PlusFive):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)


# the result seems to be consistent with super class __init__ order
foo = OneWay(5)
print('First ordering value is (5 * 2) + 5 =', foo.value)


# ----------
# swap inheritance order, but keep initialization order
class AnotherWay(MyBaseClass, PlusFive, TimesTwo):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)


# still same = 15
bar = AnotherWay(5)
print('Second ordering value is (5 * 2) + 5 =', bar.value)


# ------------------------------------------------------------------------------
# initialize super class from subclass:  diamond inheritance
# Here super class __init__ is executed many times and its result is unpredictable
# ------------------------------------------------------------------------------

# TimesSeven and PlusNine each inherit same MyBaseClass
# Here super class __init__ is executed many times and its result is unpredictable

class TimesSeven(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value *= 7

class PlusNine(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value += 9


# Define ThisWay class, which is inherit TimesSeven and PlusNine, makes MyBaseClass comes to Diamond top.
class ThisWay(TimesSeven, PlusNine):
    def __init__(self, value):
        TimesSeven.__init__(self, value)
        # Here self.value is reset and the result of TimesSeven.__init__ constructor is ignored.
        PlusNine.__init__(self, value)

foo = ThisWay(5)
print('Should be (5 * 7) + 9 = 44 but is', foo.value)

# --> 5 + 9 = 14


# ------------------------------------------------------------------------------
# super():  ensure that common super class in diamond inheritance is executed only once
#           depending on MRO (Method Resolution Order)
# ------------------------------------------------------------------------------

class MyBaseClass:
    def __init__(self, value):
        self.value = value

# Use super():  super class initialization
class TimesSevenCorrect(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.value *= 7

# Use super():  super class initialization
class PlusNineCorrect(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.value += 9

# Use super():  super class initialization
class GoodWay(TimesSevenCorrect, PlusNineCorrect):
    def __init__(self, value):
        super().__init__(value)

# ----------
# MRO
mro_str = '\n'.join(repr(cls) for cls in GoodWay.mro())

# this shows calling order. 
# TimesSevenCorrect call PlusNineCorrect, and
# PlusNineCorrect call MyBaseClass
print(mro_str)

foo = GoodWay(5)
print('Should be 7 * (5 + 9) = 98 and is', foo.value)


# ------------------------------------------------------------------------------
# super():  explicit, automatic, implicit way
# All threes are equivalent
# ------------------------------------------------------------------------------

class ExplicitTrisect(MyBaseClass):
    def __init__(self, value):
        super(ExplicitTrisect, self).__init__(value)
        self.value /= 3

assert ExplicitTrisect(9).value == 3

class AutomaticTrisect(MyBaseClass):
    def __init__(self, value):
        super(__class__, self).__init__(value)
        self.value /= 3

class ImplicitTrisect(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.value /= 3

# ----------
# All threes are equivalent
assert ExplicitTrisect(9).value == 3
assert AutomaticTrisect(9).value == 3
assert ImplicitTrisect(9).value == 3