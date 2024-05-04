#!/usr/bin/env PYTHONHASHSEED=1234 python3


# ------------------------------------------------------------------------------
# get and update value of some keys in dictionary:
# naive way 
# ------------------------------------------------------------------------------

counters = {
    'pumpernickel': 2,
    'sourdough': 1,
}

key = 'wheat'

if key in counters:
    count = counters[key]
else:
    count = 0

counters[key] = count + 1

print(counters)


# ----------
key = 'brioche'

try:
    count = counters[key]
except KeyError:
    count = 0

counters[key] = count + 1

print(counters)


# ------------------------------------------------------------------------------
# get and update value of some keys in dictionary:
# use dict.get()
# ------------------------------------------------------------------------------

key = 'multigrain'

# 0:  if no key, return this 0 value
count = counters.get(key, 0)
counters[key] = count + 1

print(counters)


# ------------------------------------------------------------------------------
# value in dictionary is list
# ------------------------------------------------------------------------------

# values are list type
votes = {
    'baguette': ['Bob', 'Alice'],
    'ciabatta': ['Coco', 'Deb'],
}

key = 'wheat'
who = 'Gertrude'

names = votes.get(key)
print(names)

if names is None:
    # this is one liner !!
    votes[key] = names = []

names.append(who)

print(votes)


# ------------------------------------------------------------------------------
# use walrus operator, more simple
# ------------------------------------------------------------------------------

key = 'brioche'
who = 'Hugh'

if (names := votes.get(key)) is None:
    votes[key] = names = []

names.append(who)

print(votes)


# ------------------------------------------------------------------------------
# setdefault() is most simple
#   try to get value for given key and return value, if no key return given defaulted value
# but some risky ...
# ------------------------------------------------------------------------------

votes = {
    'baguette': ['Bob', 'Alice'],
    'ciabatta': ['Coco', 'Deb'],
}

key = 'ciabatta'
names = votes.setdefault(key, [])
print(names)

key = 'cornbread'
names = votes.setdefault(key, [])
# return defaulted value ([])
print(names)

who = 'Kirk'
names.append(who)

# surprisingly, key and value both are set
print(votes)


# ----------
data = {}
key = 'foo'
value = []
data.setdefault(key, value)
print('Before:', data)
print('Before:', value)

# now append to value (value is list [])
value.append('hello')

# but data is also updated.
print('After: ', data)
print('After:', value)


# ----------
counters = {
    'pumpernickel': 2,
    'sourdough': 1,
}

key = 'dutch crunch'

count = counters.setdefault(key, 0)
counters[key] = count + 1

print(counters)
