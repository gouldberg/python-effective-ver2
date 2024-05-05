#!/usr/bin/env PYTHONHASHSEED=1234 python3


# ------------------------------------------------------------------------------
# Closure:  function to refer to variables within defined scope
# ------------------------------------------------------------------------------

def sort_priority(values, group):
    # helper(): closure function, can access to 'group', which scope is sort_priority()
    def helper(x):
        if x in group:
            return (0, x)
        return (1, x)
    # sort() method accept closure function helper()
    values.sort(key=helper)


numbers = [8, 3, 1, 2, 5, 4, 7, 6]

group = {2, 3, 5, 7}

sort_priority(numbers, group)

# [2, 3, 5, 7, 1, 4, 6, 8]
print(numbers)


# ------------------------------------------------------------------------------
# Closure:  = (substitution) occurs in closure, this substitution is recognized as define
# ------------------------------------------------------------------------------

def sort_priority2(numbers, group):
    found = False         # Scope: 'sort_priority2'
    def helper(x):
        if x in group:
            found = True  # Scope: 'helper' -- Bad!, this found = True is recognized as definition
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found


numbers = [8, 3, 1, 2, 5, 4, 7, 6]

found = sort_priority2(numbers, group)

# same result: [2, 3, 5, 7, 1, 4, 6, 8]
print(numbers)

# but False not True:  
print('Found:', found)


# ------------------------------------------------------------------------------
# nonlocal:  the variable scope is not local but outside
# ------------------------------------------------------------------------------

def sort_priority3(numbers, group):
    found = False
    def helper(x):
        nonlocal found  # Added
        if x in group:
            found = True
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found


numbers = [8, 3, 1, 2, 5, 4, 7, 6]

found = sort_priority3(numbers, group)

# Now the found is True
assert found

assert numbers == [2, 3, 5, 7, 1, 4, 6, 8]


# ------------------------------------------------------------------------------
# Wrap by class
# ------------------------------------------------------------------------------

numbers = [8, 3, 1, 2, 5, 4, 7, 6]

class Sorter:
    def __init__(self, group):
        self.group = group
        self.found = False

    def __call__(self, x):
        if x in self.group:
            self.found = True
            return (0, x)
        return (1, x)

sorter = Sorter(group)

numbers.sort(key=sorter)

# This sorter.found is True
assert sorter.found is True

assert numbers == [2, 3, 5, 7, 1, 4, 6, 8]