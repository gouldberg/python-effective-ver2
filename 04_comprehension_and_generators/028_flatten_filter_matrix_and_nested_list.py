#!/usr/bin/env PYTHONHASHSEED=1234 python3


matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

my_lists = [
    [[1, 2, 3], [4, 5, 6]],
    [[7, 8, 9], [10, 11, 12]],
]

a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


# ------------------------------------------------------------------------------
# flatten matrix, list
# ------------------------------------------------------------------------------

# this flatten matrix ...
flat = [x for row in matrix for x in row]
print(flat)


flat = [x for sublist1 in my_lists
        for sublist2 in sublist1
        for x in sublist2]
print(flat)


# use 'for' for simplicity
flat = []
for sublist1 in my_lists:
    for sublist2 in sublist1:
        flat.extend(sublist2)
print(flat)


# ------------------------------------------------------------------------------
# square every elements in matrix
# ------------------------------------------------------------------------------

squared = [[x**2 for x in row] for row in matrix]
print(squared)


# ------------------------------------------------------------------------------
# filtering matrix
# ------------------------------------------------------------------------------

# list comprehension
b = [x for x in a if x > 4 if x % 2 == 0]
c = [x for x in a if x > 4 and x % 2 == 0]
print(b)
print(c)
assert b and c
assert b == c


# filtering matrix
filtered = [[x for x in row if x % 3 == 0]
            for row in matrix if sum(row) >= 10]

print(filtered)
