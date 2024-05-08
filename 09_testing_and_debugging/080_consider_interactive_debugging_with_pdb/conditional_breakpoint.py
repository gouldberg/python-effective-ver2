#!/usr/bin/env PYTHONHASHSEED=1234 python3

# ------------------------------------------------------------------------------
# use pbd for debugging
# ------------------------------------------------------------------------------

# ----------
## start debugging
# python3 conditional_breakpoint.py

# ----------
## input local variable name
# err_2
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
# conditional breakpoint
#   set breakpoint() in if condition
# ------------------------------------------------------------------------------

import math

def compute_rmse(observed, ideal):
    total_err_2 = 0
    count = 0
    for got, wanted in zip(observed, ideal):
        err_2 = (got - wanted) ** 2
        if err_2 >= 1:  # Start the debugger if True
            breakpoint()
        total_err_2 += err_2
        count += 1
    mean_err = total_err_2 / count
    rmse = math.sqrt(mean_err)
    return rmse

result = compute_rmse(
    [1.8, 1.7, 3.2, 7],
    [2, 1.5, 3, 5])

print(result)
