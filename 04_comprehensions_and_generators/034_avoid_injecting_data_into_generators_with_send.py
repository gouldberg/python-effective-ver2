#!/usr/bin/env PYTHONHASHSEED=1234 python3

import math

# ------------------------------------------------------------------------------
# generate wave like values given amplitude 
# ------------------------------------------------------------------------------

def wave(amplitude, steps):
    step_size = 2 * math.pi / steps
    for step in range(steps):
        radians = step * step_size
        fraction = math.sin(radians)
        output = amplitude * fraction
        yield output

def transmit(output):
    if output is None:
        print(f'Output is None')
    else:
        print(f'Output: {output:>5.1f}')

def run(it):
    for output in it:
        transmit(output)

run(wave(3.0, 8))


# ------------------------------------------------------------------------------
# this is just boiler plate 
# ------------------------------------------------------------------------------

def my_generator():
    received = yield 1
    print(f'received = {received}')

it = my_generator()

output = next(it)       # Get first generator output

print(f'output = {output}')

# next(it) print:  received = None
try:
    next(it)            # Run generator until it exits
except StopIteration:
    pass
else:
    assert False


# ------------------------------------------------------------------------------
# send value into the generator (update yield value, at the time)
# ------------------------------------------------------------------------------

it = my_generator()

output = it.send(None)  # Get first generator output

print(f'output = {output}')

# now send value into the generator by it.send('XXX')
# now it.send('hello!) print:  received = hello!
try:
    it.send('hello!')
except StopIteration:
    pass
else:
    assert False


# ------------------------------------------------------------------------------
# update amplitude dependent on input signal
# use send
# ------------------------------------------------------------------------------

def wave_modulating(steps):
    step_size = 2 * math.pi / steps
    amplitude = yield             # Receive initial amplitude
    for step in range(steps):
        radians = step * step_size
        fraction = math.sin(radians)
        output = amplitude * fraction
        amplitude = yield output  # Receive next amplitude


def run_modulating(it):
    amplitudes = [
        None, 7, 7, 7, 2, 2, 2, 2, 10, 10, 10, 10, 10]
    for amplitude in amplitudes:
        # ----------
        # send here.
        output = it.send(amplitude)
        transmit(output)


run_modulating(wave_modulating(12))


# --> good but first output is None, since generator does not take input at first.


# ------------------------------------------------------------------------------
# complex wave:  use yield from and send
# ------------------------------------------------------------------------------

def complex_wave():
    yield from wave(7.0, 3)
    yield from wave(2.0, 4)
    yield from wave(10.0, 5)

run(complex_wave())


# ----------
def complex_wave_modulating():
    yield from wave_modulating(3)
    yield from wave_modulating(4)
    yield from wave_modulating(5)

run_modulating(complex_wave_modulating())


# --> output None ...


# ------------------------------------------------------------------------------
# not use send,
# but pass iterator to wave function
# ------------------------------------------------------------------------------

# amplitude_it is iterator
def wave_cascading(amplitude_it, steps):
    step_size = 2 * math.pi / steps
    for step in range(steps):
        radians = step * step_size
        fraction = math.sin(radians)
        amplitude = next(amplitude_it)  # Get next input
        output = amplitude * fraction
        yield output


def complex_wave_cascading(amplitude_it):
    yield from wave_cascading(amplitude_it, 3)
    yield from wave_cascading(amplitude_it, 4)
    yield from wave_cascading(amplitude_it, 5)


def run_cascading():
    amplitudes = [7, 7, 7, 2, 2, 2, 2, 10, 10, 10, 10, 10]
    # iterator is passed
    it = complex_wave_cascading(iter(amplitudes))
    for amplitude in amplitudes:
        output = next(it)
        transmit(output)

run_cascading()


# --> no None ...
# NOTE: this code assumes input generator is thread safe.
