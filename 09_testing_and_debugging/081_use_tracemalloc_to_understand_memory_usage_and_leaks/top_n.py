#!/usr/bin/env PYTHONHASHSEED=1234 python3

# python3 top_n.py

import tracemalloc


# ------------------------------------------------------------------------------
# tracemalloc to understand 
# how the object is assigned. 
# ------------------------------------------------------------------------------

# set stack depth
tracemalloc.start(10)

# before snapshot
time1 = tracemalloc.take_snapshot()


# ----------
# here import
import waste_memory

# usage to debug
x = waste_memory.run()

# after snapshot
time2 = tracemalloc.take_snapshot()


# ----------
# compare snapshots
stats = time2.compare_to(time1, 'lineno')

# show top3
for stat in stats[:3]:
    print(stat)
