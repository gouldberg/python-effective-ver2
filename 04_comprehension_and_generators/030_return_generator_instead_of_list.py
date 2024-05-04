#!/usr/bin/env PYTHONHASHSEED=1234 python3


# ------------------------------------------------------------------------------
# return list
# ------------------------------------------------------------------------------

def index_words(text):
    result = []
    if text:
        result.append(0)
    for index, letter in enumerate(text):
        if letter == ' ':
            result.append(index + 1)
    return result


address = 'Four score and seven years ago...'
address = 'Four score and seven years ago our fathers brought forth on this continent a new nation, conceived in liberty, and dedicated to the proposition that all men are created equal.'

result = index_words(address)

print(result[:10])


# -->
# This code have 2 problems:
#  1.  complex, not readable
#  2.  require to append all index, leading to memory consumption, if input is large text.


# ------------------------------------------------------------------------------
# use generator for simplicity
# ------------------------------------------------------------------------------

def index_words_iter(text):
    if text:
        yield 0
    for index, letter in enumerate(text):
        if letter == ' ':
            yield index + 1


it = index_words_iter(address)
print(next(it))
print(next(it))


# ----------
result = list(index_words_iter(address))
print(result[:10])


# ------------------------------------------------------------------------------
# stream generator
# ------------------------------------------------------------------------------

address_lines = """Four score and seven years
ago our fathers brought forth on this
continent a new nation, conceived in liberty,
and dedicated to the proposition that all men
are created equal."""

# write this text to file.
with open('00_tmp/address.txt', 'w') as f:
    f.write(address_lines)


# ----------
def index_file(handle):
    offset = 0
    for line in handle:
        if line:
            yield offset
        for letter in line:
            offset += 1
            if letter == ' ':
                yield offset

import itertools

# read text
with open('00_tmp/address.txt', 'r') as f:
    it = index_file(f)
    results = itertools.islice(it, 0, 10)
    print(list(results))

