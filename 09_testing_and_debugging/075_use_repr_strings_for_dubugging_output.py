#!/usr/bin/env PYTHONHASHSEED=1234 python3


# ------------------------------------------------------------------------------
# print 
# ------------------------------------------------------------------------------

print('foo bar')


# ----------
my_value = 'foo bar'

# all outputs are equivalent
my_value
str(my_value)
'%s' % my_value
f'{my_value}'
format(my_value)
my_value.__format__('s')
my_value.__str__()


# ------------------------------------------------------------------------------
# problem:  integer and string is same output by print
# ------------------------------------------------------------------------------

print(5)
print('5')

int_value = 5
str_value = '5'
print(f'{int_value} == {str_value} ?')


# ------------------------------------------------------------------------------
# use repr() in debugging
# ------------------------------------------------------------------------------

a = '\x07'
print(repr(a))


# eval converts to python object
b = eval(repr(a))
assert a == b


# in debugging, print should be used with repr
print(repr(5))
print(repr('5'))


# followings are same as print(repr())
# %r + %
print('%r' % 5)
print('%r' % '5')

# f-string + !r
int_value = 5
str_value = '5'
print(f'{int_value!r} != {str_value!r}')


# ------------------------------------------------------------------------------
# implement __repr__ in my class for readable class
# ------------------------------------------------------------------------------

class OpaqueClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y

obj = OpaqueClass(1, 'foo')

# not readable
print(obj)

# access to __dict__
print(obj.__dict__)


# ----------
# __repr__ implemented
class BetterClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # use __repr__
    def __repr__(self):
        # return python expression
        return f'BetterClass({self.x!r}, {self.y!r})'

obj = BetterClass(2, 'bar')
print(obj)
