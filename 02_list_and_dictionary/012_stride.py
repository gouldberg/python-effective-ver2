#!/usr/bin/env PYTHONHASHSEED=1234 python3


# ------------------------------------------------------------------------------
# stride
# ------------------------------------------------------------------------------

x = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']

odds = x[::2]
evens = x[1::2]

print(odds)
print(evens)


# ------------------------------------------------------------------------------
# reverse sequence
# ------------------------------------------------------------------------------

x = b'mongoose'
y = x[::-1]

print(y)


# ----------
# this reverse works Unicode 
x = '寿司'
y = x[::-1]

print(y)


# ----------
# this reverse DOES NOT work Unicode data encoded by UTF-8 byte string
w = '寿司'
x = w.encode('utf-8')
y = x[::-1]
print(x)
print(y)

# but UnicodeDecodeError
z = y.decode('utf-8')


# ------------------------------------------------------------------------------
# negative stride, slice + stride
# ------------------------------------------------------------------------------

x = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
x[::2]   # ['a', 'c', 'e', 'g']
x[::-2]  # ['h', 'f', 'd', 'b']


# slice + stride will produce shallow copy inside.
# If you use itertools.islice is more efficient but does not allow negative value at start, end, stride. --> see 036

x[2::2]     # ['c', 'e', 'g']
x[-2::-2]   # ['g', 'e', 'c', 'a']
x[-2:2:-2]  # ['g', 'e']
x[2:2:-2]   # []


y = x[::2]   # ['a', 'c', 'e', 'g']
z = y[1:-1]  # ['c', 'e']
print(x)
print(y)
print(z)
