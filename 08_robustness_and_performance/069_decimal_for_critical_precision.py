#!/usr/bin/env PYTHONHASHSEED=1234 python3

from decimal import Decimal
from decimal import ROUND_UP


# ------------------------------------------------------------------------------
# double float (IEEE754) 
# ------------------------------------------------------------------------------

rate = 1.45
seconds = 3*60 + 42
cost = rate * seconds / 60

# double float (IEEE754) short of 0.0001
# true value is 5.365
print(cost)

# if rounded, 5.36
print(round(cost, 2))


# ------------------------------------------------------------------------------
# use Decimal
# ------------------------------------------------------------------------------

rate = Decimal('1.45')

seconds = Decimal(3*60 + 42)

cost = rate * seconds / Decimal(60)

# true value (= 5.365)
print(cost)


# ------------------------------------------------------------------------------
# set value of Decimal instance
# ------------------------------------------------------------------------------

# set by string:  no precision loss
print(Decimal('1.45'))

# set by float:  precision loss
print(Decimal(1.45))

# set by integer:  no precision loss
print(Decimal(2))


# 1/3 is approximated.
# --> if you really are required to use rational number without precision loss,
#     use fractions.Fraction
print(Decimal(1/3))


# ------------------------------------------------------------------------------
# small value rounding up
# ------------------------------------------------------------------------------

rate = Decimal('0.05')

seconds = Decimal('5')

small_cost = rate * seconds / Decimal(60)

print(small_cost)


# small value is rounded to zero
print(round(small_cost, 2))


# rounding up, specifying the rounding level
rounded = cost.quantize(Decimal('0.01'), rounding=ROUND_UP)
print(round(cost, 2))
print(f'Rounded {cost} to {rounded}')


rounded = small_cost.quantize(Decimal('0.01'), rounding=ROUND_UP)
print(round(small_cost, 2))
print(f'Rounded {small_cost} to {rounded}')
