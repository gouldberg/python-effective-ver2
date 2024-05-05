#!/usr/bin/env PYTHONHASHSEED=1234 python3


# ------------------------------------------------------------------------------
# positional and keyword arguments 
# ------------------------------------------------------------------------------

def remainder(number, divisor):
    return number % divisor

assert remainder(20, 7) == 6


# ----------
# OK
remainder(20, 7)
remainder(20, divisor=7)
remainder(number=20, divisor=7)
remainder(divisor=7, number=20)


# Those will not compile
# positional arguments (7) should be before keyword arguments (number=20) 
remainder(number=20, 7)

# argument value can be set only once
remainder(20, number=7)


# ------------------------------------------------------------------------------
# arguments can be passed by dictionary
# ------------------------------------------------------------------------------

my_kwargs = {
	'number': 20,
	'divisor': 7,
}

# use **
assert remainder(**my_kwargs) == 6


# ----------
my_kwargs = {
	'divisor': 7,
}

assert remainder(number=20, **my_kwargs) == 6


# ----------
my_kwargs = {
	'number': 20,
}

other_kwargs = {
	'divisor': 7,
}

assert remainder(**my_kwargs, **other_kwargs) == 6


# ------------------------------------------------------------------------------
# **kwargs can accept multiple all keyword variables and recognized as dictionary in the function
# ------------------------------------------------------------------------------

def print_parameters(**kwargs):
    # kwargs recognized as dictionary
    for key, value in kwargs.items():
        print(f'{key} = {value}')


# pass multiple keyword variables
print_parameters(alpha=1.5, beta=9, gamma=4)


# ------------------------------------------------------------------------------
# default value for keyword argument
# ------------------------------------------------------------------------------

def flow_rate(weight_diff, time_diff):
    return weight_diff / time_diff

weight_diff = 0.5
time_diff = 3

flow = flow_rate(weight_diff, time_diff)
print(f'{flow:.3} kg per second')


# ----------
def flow_rate(weight_diff, time_diff, period):
    return (weight_diff / time_diff) * period

flow_per_second = flow_rate(weight_diff, time_diff, 1)


# ----------
# set default value 1 to keyword argument period
def flow_rate(weight_diff, time_diff, period=1):
    return (weight_diff / time_diff) * period

flow_per_second = flow_rate(weight_diff, time_diff)
flow_per_hour = flow_rate(weight_diff, time_diff, period=3600)
print(flow_per_second)
print(flow_per_hour)


# ------------------------------------------------------------------------------
# default value for keyword argument
# ------------------------------------------------------------------------------

def flow_rate(weight_diff, time_diff,
              period=1, units_per_kg=1):

    return ((weight_diff * units_per_kg) / time_diff) * period


pounds_per_hour = flow_rate(weight_diff, time_diff,
                            period=3600, units_per_kg=2.2)
print(pounds_per_hour)


# optional keyword arguments can be set as like positional arguments
pounds_per_hour = flow_rate(weight_diff, time_diff, 3600, 2.2)
print(pounds_per_hour)