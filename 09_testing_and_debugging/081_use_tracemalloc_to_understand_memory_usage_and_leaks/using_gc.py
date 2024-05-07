#!/usr/bin/env PYTHONHASHSEED=1234 python3

# python3 using_gc.py

import gc


# ------------------------------------------------------------------------------
# gc.get_objects() show objects
# but does not show how the object is assigned. 
# ------------------------------------------------------------------------------

found_objects = gc.get_objects()
print('Before:', len(found_objects))


# ----------
# here import
import waste_memory

hold_reference = waste_memory.run()

found_objects = gc.get_objects()
print('After: ', len(found_objects))
for obj in found_objects[:3]:
    print(repr(obj)[:100])

print('...')
