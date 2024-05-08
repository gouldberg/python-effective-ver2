#!/usr/bin/env PYTHONHASHSEED=1234 python3

# ------------------------------------------------------------------------------
# pdb.pm()
# debugging in interactive python interpreter
# ------------------------------------------------------------------------------

# python3

# import my_mymodule

# my_module.compute_stddev([5])
## --> here ZeroDivisionError

## start pdb.pm()
# import pdb; pdb.pm()

## (pdb) prompt is shown 
# (pdb) err_2_sum

# (pdb) len(data)


# ------------------------------------------------------------------------------
# my module
# ------------------------------------------------------------------------------

import math

def squared_error(point, mean):
    err = point - mean
    return err ** 2

def compute_variance(data):
    mean = sum(data) / len(data)
    err_2_sum = sum(squared_error(x, mean) for x in data)
    variance = err_2_sum / (len(data) - 1)
    return variance

def compute_stddev(data):
    variance = compute_variance(data)
    return math.sqrt(variance)
