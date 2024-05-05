#!/usr/bin/env PYTHONHASHSEED=1234 python3


# ------------------------------------------------------------------------------
# bytes:  raw, no sign, 8 bit, normally ASCII encoded
#  - bytes instance does not have text encoding
# ------------------------------------------------------------------------------

a = b'h\x65llo'

print(list(a))

print(a)


# ------------------------------------------------------------------------------
# str:  include Unicode code point
#  - str instance does not have binary encoding
# ------------------------------------------------------------------------------

a = 'a\u0300 propos'

print(list(a))

print(a)


# ------------------------------------------------------------------------------
# convert bytes to str by decode('utf-8')
# ------------------------------------------------------------------------------

def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value  # Instance of str

value = b'foo'.decode('utf-8')

print(repr(to_str(b'foo')))

print(repr(to_str('bar')))


# ------------------------------------------------------------------------------
# convert str to bytes by encode('utf-8')
# ------------------------------------------------------------------------------

def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode('utf-8')
    else:
        value = bytes_or_str
    return value  # Instance of bytes

value = 'bar'.encode('utf-8')

print(repr(to_bytes(b'foo')))

print(repr(to_bytes('bar')))


# ------------------------------------------------------------------------------
# concatenation
# ------------------------------------------------------------------------------

# OK: bytes + bytes
print(b'one' + b'two')

# OK: str + str
print('one' + 'two')

# NG: bytes + str  --> TypeError
b'one' + 'two'

# NG: str + bytes  --> TypeError
'one' + b'two'


# ------------------------------------------------------------------------------
# comparison
# ------------------------------------------------------------------------------

# can compare
assert b'red' > b'blue'

# can compare
assert 'red' > 'blue'

# can NOT compare
assert 'red' > b'blue'

# can NOT compare
assert b'blue' < 'red'

# False but the reason is not value but type
print(b'foo' == 'boo')


# ------------------------------------------------------------------------------
# formatting
# ------------------------------------------------------------------------------

# OK
print(b'red %s' % b'blue')

# OK
print('red %s' % 'blue')

# TypeError
print(b'red %s' % 'blue')

# OK but replaced by bytes instance
print('red %s' % b'blue')


# ------------------------------------------------------------------------------
# file read
# ------------------------------------------------------------------------------

# Silently force UTF-8 here to make sure this test fails on
# all platforms. cp1252 considers these bytes valid on Windows.
real_open = open

def open(*args, **kwargs):
    kwargs['encoding'] = 'utf-8'
    return real_open(*args, **kwargs)

with open('data.bin', 'r') as f:
    data = f.read()


# Restore the overloaded open above.
open = real_open

# read by binary mode
with open('data.bin', 'rb') as f:
    data = f.read()

assert data == b'\xf1\xf2\xf3\xf4\xf5'


with open('data.bin', 'r', encoding='cp1252') as f:
    data = f.read()

assert data == 'ñòóôõ'
