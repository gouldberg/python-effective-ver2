#!/usr/bin/env PYTHONHASHSEED=1234 python3

import time
import select
import socket

from threading import Thread


# ------------------------------------------------------------------------------
# factorize:  normal sequential computation
# ------------------------------------------------------------------------------

def factorize(number):
    for i in range(1, number + 1):
        if number % i == 0:
            yield i


numbers = [2139079, 1214759, 1516637, 1852285]


start = time.time()

for number in numbers:
    list(factorize(number))

end = time.time()
delta = end - start

# 0.418 secs
print(f'Took {delta:.3f} seconds')


# ------------------------------------------------------------------------------
# factorize:  use thread each by given input
# ------------------------------------------------------------------------------

class FactorizeThread(Thread):
    def __init__(self, number):
        super().__init__()
        self.number = number

    def run(self):
        self.factors = list(factorize(self.number))


start = time.time()

threads = []

for number in numbers:
    thread = FactorizeThread(number)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

end = time.time()
delta = end - start

# but this takes 0.857 secs !!!
print(f'Took {delta:.3f} seconds')


# ------------------------------------------------------------------------------
# Blocking IO:  normal sequential operation
# ------------------------------------------------------------------------------

# slow speed system call (select)
# this function require 0.1 sec blocking to OS and back to program

def slow_systemcall():
    select.select([socket.socket()], [], [], 0.1)


start = time.time()

num = 1000
for _ in range(num):
    slow_systemcall()

end = time.time()
delta = end - start

# 0.041 secs
print(f'Took {delta:.3f} seconds')


# ------------------------------------------------------------------------------
# Blocking IO:  compute while communicating with helicopter (multiple serial port)
# ------------------------------------------------------------------------------

# now blocking 1.0 secs
def slow_systemcall():
    select.select([socket.socket()], [], [], 1.0)

num = 100
threads = []

start = time.time()

for _ in range(num):
    thread = Thread(target=slow_systemcall)
    thread.start()
    threads.append(thread)


def compute_helicopter_location(index):
    for number in numbers:
        list(factorize(number))
    # pass

for i in range(num):
    compute_helicopter_location(i)

for thread in threads:
    thread.join()

end = time.time()
delta = end - start

# only 32.277 secs
print(f'Took {delta:.3f} seconds')