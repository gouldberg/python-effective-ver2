#!/usr/bin/env PYTHONHASHSEED=1234 python3

from collections import defaultdict
import logging


# ------------------------------------------------------------------------------
# dict.get() 
# ------------------------------------------------------------------------------

# ----------
# prepare png file
path = '00_tmp/profile_1234.png'

with open(path, 'wb') as f:
    f.write(b'image data here 1234')


# -----------
pictures = {}
print(pictures.get(path))

if (handle := pictures.get(path)) is None:
    try:
        handle = open(path, 'a+b')
    except OSError:
        print(f'Failed to open path {path}')
        raise
    else:
        pictures[path] = handle

# now pictures get open handle
print(pictures)

handle.seek(0)
image_data = handle.read()

print(image_data)


# ------------------------------------------------------------------------------
# Examples using in and KeyError
# ------------------------------------------------------------------------------

# ----------
path = '00_tmp/profile_9991.png'

with open(path, 'wb') as f:
    f.write(b'image data here 9991')


# ----------
pictures = {}

if path in pictures:
    handle = pictures[path]
else:
    try:
        handle = open(path, 'a+b')
    except OSError:
        print(f'Failed to open path {path}')
        raise
    else:
        pictures[path] = handle

handle.seek(0)

image_data = handle.read()

print(pictures)
print(image_data)


# ------------------------------------------------------------------------------
# Examples using nested try/except and KeyError
# ------------------------------------------------------------------------------

# ----------
path = '00_tmp/profile_9922.png'

with open(path, 'wb') as f:
    f.write(b'image data here 9991')

# ----------
pictures = {}

try:
    handle = pictures[path]
except KeyError:
    try:
        handle = open(path, 'a+b')
    except OSError:
        print(f'Failed to open path {path}')
        raise
    else:
        pictures[path] = handle

handle.seek(0)
image_data = handle.read()

print(pictures)
print(image_data)


# ------------------------------------------------------------------------------
# setdefault()
# ------------------------------------------------------------------------------

# ----------
path = '00_tmp/profile_9239.png'

with open(path, 'wb') as f:
    f.write(b'image data here 9239')


# ----------
# even if path exists in pictures dictionary, open is called.
pictures = {}

try:
    handle = pictures.setdefault(path, open(path, 'a+b'))
except OSError:
    print(f'Failed to open path {path}')
    raise
else:
    handle.seek(0)
    image_data = handle.read()

print(pictures)
print(image_data)


# ------------------------------------------------------------------------------
# defaultdict() can not accept function with arguments
# ------------------------------------------------------------------------------

try:
    path = '00_tmp/profile_4555.csv'
    
    with open(path, 'wb') as f:
        f.write(b'image data here 9239')
    
    def open_picture(profile_path):
        try:
            return open(profile_path, 'a+b')
        except OSError:
            print(f'Failed to open path {profile_path}')
            raise

    # TypeError, since
    # open_picture requires argument (profile_path) and
    # defaultdict can not accept functions with arguments
    pictures = defaultdict(open_picture)
    handle = pictures[path]
    handle.seek(0)
    image_data = handle.read()
except:
    logging.exception('Expected')
else:
    assert False


# ------------------------------------------------------------------------------
# class with __missing__
# __missing__ can handle key dependent default value
# ------------------------------------------------------------------------------

path = '00_tmp/account_9090.csv'

with open(path, 'wb') as f:
    f.write(b'image data here 9090')

def open_picture(profile_path):
    try:
        return open(profile_path, 'a+b')
    except OSError:
        print(f'Failed to open path {profile_path}')
        raise

class Pictures(dict):
    def __missing__(self, key):
        value = open_picture(key)
        self[key] = value
        return value

pictures = Pictures()

handle = pictures[path]
handle.seek(0)

image_data = handle.read()

print(pictures)
print(image_data)
