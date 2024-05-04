#!/usr/bin/env PYTHONHASHSEED=1234 python3

# list, str, bytes are easy to be sliced.
# Slice is applicable to Python class implementing special method __getitem__ and __setitem__


a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']


# ------------------------------------------------------------------------------
# variety of slices
# ------------------------------------------------------------------------------

print('Middle two:  ', a[3:5])

print('All but ends:', a[1:7])


# ----------
assert a[:5] == a[0:5]


# ----------
assert a[5:] == a[5:len(a)]


# ----------
print(a[:])
print(a[:5])
print(a[:-1])
print(a[4:])
print(a[-3:])
print(a[2:5])
print(a[2:-1])
print(a[-3:-1])


# ----------
a[:]      # ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
a[:5]     # ['a', 'b', 'c', 'd', 'e']
a[:-1]    # ['a', 'b', 'c', 'd', 'e', 'f', 'g']
a[4:]     #                     ['e', 'f', 'g', 'h']
a[-3:]    #                          ['f', 'g', 'h']
a[2:5]    #           ['c', 'd', 'e']
a[2:-1]   #           ['c', 'd', 'e', 'f', 'g']
a[-3:-1]  #                          ['f', 'g']


# ------------------------------------------------------------------------------
# access by slicing or directly to index more than length
# ------------------------------------------------------------------------------

# by slicing:  20 > length(a) but access is possible
first_twenty_items = a[:20]
last_twenty_items = a[-20:]

print(first_twenty_items)
print(last_twenty_items)


# this will produce IndexError
print(a[20])


# ------------------------------------------------------------------------------
# sliced result is new list
# ------------------------------------------------------------------------------

b = a[3:]
print('Before:   ', b)

b[1] = 99
print('After:    ', b)

# original a is not changed
print('No change:', a)


# ------------------------------------------------------------------------------
# assignment (substitution ?) by different length
# ------------------------------------------------------------------------------

a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
print('Before ', a)

# 5 elements vs. 3 elements
a[2:7] = [99, 22, 14]

# the length is shorter than original a
print('After  ', a)


# ----------
a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
print('Before ', a)

# only 1 element vs. 2 elements
a[2:3] = [47, 11]

# the length will be longer
print('After  ', a)


# ------------------------------------------------------------------------------
# copy original
# ------------------------------------------------------------------------------

a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

b = a[:]

assert b == a and b is not a


# ------------------------------------------------------------------------------
# no slice
# ------------------------------------------------------------------------------

a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

b = a
print('Before a', a)
print('Before b', b)

a[:] = [101, 102, 103]
assert a is b             # Still the same list object

print('After a ', a)      # Now has different contents
print('After b ', b)      # Same list, so same contents as a
