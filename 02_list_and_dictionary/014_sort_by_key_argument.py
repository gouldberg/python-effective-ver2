#!/usr/bin/env PYTHONHASHSEED=1234 python3


# ------------------------------------------------------------------------------
# naive sort
# ------------------------------------------------------------------------------

numbers = [93, 86, 11, 68, 70]

numbers.sort()

print(numbers)


# ------------------------------------------------------------------------------
# sort() does not apply
# ------------------------------------------------------------------------------

class Tool:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def __repr__(self):
        return f'Tool({self.name!r}, {self.weight})'

tools = [
    Tool('level', 3.5),
    Tool('hammer', 1.25),
    Tool('screwdriver', 0.5),
    Tool('chisel', 0.25),
]

# sort() does not apply to Tool class
tools.sort()

print('Unsorted:', repr(tools))


# ------------------------------------------------------------------------------
# give key argument to sort()
# sort by object's attribute
# ------------------------------------------------------------------------------

tools.sort(key=lambda x: x.name)

print('\nSorted:  ', tools)


tools.sort(key=lambda x: x.weight)

print('By weight:', tools)


# ------------------------------------------------------------------------------
# Can apply some preprocessing before sorting
# ------------------------------------------------------------------------------

places = ['home', 'work', 'New York', 'Paris']

places.sort()
print('Case sensitive:  ', places)

# preprocess:  lower()
places.sort(key=lambda x: x.lower())
print('Case insensitive:', places)


# ------------------------------------------------------------------------------
# apply multiple sorting criteria
# give tuple to key argument
# ------------------------------------------------------------------------------

# Tuple can be compared (implemented such as by __lt__ to be applicable to sort())
saw = (5, 'circular saw')
jackhammer = (40, 'jackhammer')
assert not (jackhammer < saw)  # Matches expectations

drill = (4, 'drill')
sander = (4, 'sander')
assert drill[0] == sander[0]  # Same weight
assert drill[1] < sander[1]   # Alphabetically less
assert drill < sander         # Thus, drill comes first


# ----------
power_tools = [
    Tool('drill', 4),
    Tool('circular saw', 5),
    Tool('jackhammer', 40),
    Tool('sander', 4),
]

# sort by weight(first), name(second)
# give tuple to key argument
power_tools.sort(key=lambda x: (x.weight, x.name))
print(power_tools)


# reverse: makes all criteria descending
power_tools.sort(key=lambda x: (x.weight, x.name), reverse=True)
print(power_tools)


# only weight is descending
power_tools.sort(key=lambda x: (-x.weight, x.name))
print(power_tools)


# try only name is descending --> can not be applicable to string
power_tools.sort(key=lambda x: (x.weight, -x.name),
                     reverse=True)


# ------------------------------------------------------------------------------
# apply multiple sorting criteria:  sequentially
# ------------------------------------------------------------------------------

# if key value is equal, preserve the order.

power_tools = [
    Tool('drill', 4),
    Tool('circular saw', 5),
    Tool('jackhammer', 40),
    Tool('sander', 4),
]

# 1st: name ascending (weight for drill and sander is same 4, now drill comes first)
power_tools.sort(key=lambda x: x.name)
print(power_tools)

# 2nd: weight descending --> sander comes after drill.
power_tools.sort(key=lambda x: x.weight, reverse=True)
print(power_tools)
