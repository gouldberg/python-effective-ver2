#!/usr/bin/env PYTHONHASHSEED=1234 python3

import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor


# ------------------------------------------------------------------------------
# gcd
# ------------------------------------------------------------------------------

def gcd(pair):
    a, b = pair
    low = min(a, b)
    for i in range(low, 0, -1):
        if a % i == 0 and b % i == 0:
            return i
    assert False, 'Not reachable'


NUMBERS = [
    (1963309, 2265973), (2030677, 3814172),
    (1551645, 2229620), (2039045, 2020802),
    (1823712, 1924928), (2293129, 1020491),
    (1281238, 2273782), (3823812, 4237281),
    (3812741, 4729139), (1292391, 2123811),
]


# ------------------------------------------------------------------------------
# Run serial
# ------------------------------------------------------------------------------

def main():
    start = time.time()
    results = list(map(gcd, NUMBERS))
    end = time.time()
    delta = end - start
    print(f'Took {delta:.3f} seconds')


# 1.028 secs
main()


# ------------------------------------------------------------------------------
# Run threads by concurrent.futures.ThreadPoolExecutor
# ------------------------------------------------------------------------------

def main():    
    start = time.time()
    pool = ThreadPoolExecutor(max_workers=2)
    results = list(pool.map(gcd, NUMBERS))
    end = time.time()
    delta = end - start
    print(f'Took {delta:.3f} seconds')


# 1.141 secs, slower ..., due to overhead for starting thread pool and communication
main()


# ------------------------------------------------------------------------------
# Run parallel by concurrent.futures.ProcessPoolExecutor
#
# ProcessPoolExecutor is doing ..
#  1. serialize input data to binary data by pickle module
#  2. copy serialized data from main interpreter process to child interpreter process via socket.
#  3. by child process pickle, deserialize data to python object
#  4. execute in parallel with other child processes gcd func as input
#  5. deserialize the result to bytes
#  6. via socket, copy bytes and return
#  7. deserialize the bytes and return to python object at parent process
#  8. combine results from child processes into single list and return
# ------------------------------------------------------------------------------

def main():    
    start = time.time()
    pool = ProcessPoolExecutor(max_workers=2)  # The one change
    results = list(pool.map(gcd, NUMBERS))
    end = time.time()
    delta = end - start
    print(f'Took {delta:.3f} seconds')


# 0.571 secs
main()
