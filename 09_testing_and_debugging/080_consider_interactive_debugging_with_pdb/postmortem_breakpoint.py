#!/usr/bin/env PYTHONHASHSEED=1234 python3

# ------------------------------------------------------------------------------
# use pbd for debugging
# under pdb control, execute program, if program itself crashes.
# ------------------------------------------------------------------------------

# ----------
## start debugging
## under pdb control, execute postmortem_breakpoint.py
# python3 -m pdb -c continue postmortem_breakpoint.py
# 

# ----------
## input local variable name
# mean_err
# got

# ----------
## locals() show all local variables
# locals()

# ----------
## commands
# where
# up
# down
# step
# next
# return
# continue

# ----------
## quit debugging
# quit


# ------------------------------------------------------------------------------
# this program crashes whe compute_rmse is given complex number (here 7j)
# ------------------------------------------------------------------------------

import math

def compute_rmse(observed, ideal):
    total_err_2 = 0
    count = 0
    for got, wanted in zip(observed, ideal):
        err_2 = (got - wanted) ** 2
        total_err_2 += err_2
        count += 1

    mean_err = total_err_2 / count
    rmse = math.sqrt(mean_err)
    return rmse

result = compute_rmse(
    [1.8, 1.7, 3.2, 7j],  # Bad input
    [2, 1.5, 3, 5])

print(result)
