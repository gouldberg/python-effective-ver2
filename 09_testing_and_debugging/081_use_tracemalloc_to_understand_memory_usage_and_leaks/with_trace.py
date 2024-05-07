#!/usr/bin/env PYTHONHASHSEED=1234 python3

# python3 with_trace.py

import tracemalloc


# ------------------------------------------------------------------------------
# tracemalloc to understand 
# how the object is assigned. 
# ------------------------------------------------------------------------------

tracemalloc.start(10)
time1 = tracemalloc.take_snapshot()


# ----------
# here import
import waste_memory

x = waste_memory.run()

time2 = tracemalloc.take_snapshot()

stats = time2.compare_to(time1, 'traceback')


# ----------
top = stats[0]

print('Biggest offender is:')

print('\n'.join(top.traceback.format()))
