#!/usr/bin/env PYTHONHASHSEED=1234 python3

import logging
import json


# ------------------------------------------------------------------------------
# finally:  always runs after try block (such as file handler)
# ------------------------------------------------------------------------------

def try_finally_example(filename):
    print('* Opening file')
    # ----------
    # open should be before try. Exception such as IOError should skip finally block.
    handle = open(filename, encoding='utf-8') # May raise OSError
    try:
        print('* Reading data')
        # may raise UnicodeDecodeError
        return handle.read()
    finally:
        # always runs after try block
        print('* Calling close()')
        handle.close()


try:
    filename = '00_tmp/random_data.txt'
    
    with open(filename, 'wb') as f:
        f.write(b'\xf1\xf2\xf3\xf4\xf5')  # Invalid utf-8
    
    # UnicodeDecodeError.
    data = try_finally_example(filename)
    # This should not be reached.
    import sys
    sys.exit(1)
except:
    logging.exception('Expected')
else:
    assert False


# ----------
# now not UnicodeDecodeError (after read), IOError at open 
try:
    try_finally_example('does_not_exist.txt')
except:
    logging.exception('Expected')
else:
    assert False


# ------------------------------------------------------------------------------
# try/except/else makes clear which exception is raised,
# makes clear exception communication.
# ------------------------------------------------------------------------------

def load_json_key(data, key):
    try:
        print('* Loading JSON data')
        # may raise Value Error
        result_dict = json.loads(data)
    except ValueError as e:
        print('* Handling ValueError')
        raise KeyError(key) from e
    else:
        print('* Looking up key')
        # may raise KeyError
        return result_dict[key]

# ----------
# OK case
assert load_json_key('{"foo": "bar"}', 'foo') == 'bar'


# ----------
# KeyError
try:
    load_json_key('{"foo": bad payload', 'foo')
except:
    logging.exception('Expected')
else:
    assert False

# ----------
# error at result_dict[key]
try:
    load_json_key('{"foo": "bar"}', 'does not exist')
except:
    logging.exception('Expected')
else:
    assert False


# ------------------------------------------------------------------------------
# try/except/else/finally
#   else:  minimize try block to make clear what is successful.
#          else block do additional tasks after successful try and before finally.
# ------------------------------------------------------------------------------

UNDEFINED = object()
DIE_IN_ELSE_BLOCK = False

def divide_json(path):
    print('* Opening file')
    handle = open(path, 'r+')   # May raise OSError
    try:
        print('* Reading data')
        data = handle.read()    # May raise UnicodeDecodeError
        print('* Loading JSON data')
        op = json.loads(data)   # May raise ValueError
        print('* Performing calculation')
        value = (
            op['numerator'] /
            op['denominator'])  # May raise ZeroDivisionError
    except ZeroDivisionError as e:
        print('* Handling ZeroDivisionError')
        return UNDEFINED
    else:
        print('* Writing calculation')
        op['result'] = value
        result = json.dumps(op)
        handle.seek(0)          # May raise OSError
        # simulate hard disk is full.
        if DIE_IN_ELSE_BLOCK:
            import errno
            import os
            raise OSError(errno.ENOSPC, os.strerror(errno.ENOSPC))
        handle.write(result)    # May raise OSError
        return value
    finally:
        print('* Calling close()')
        handle.close()          # Always runs


temp_path = '00_tmp/random_data.json'


# ----------
# OK: try + else + finally
with open(temp_path, 'w') as f:
    f.write('{"numerator": 1, "denominator": 10}')

assert divide_json(temp_path) == 0.1


# ----------
# ZeroDivisionError: try + except + finally
with open(temp_path, 'w') as f:
    f.write('{"numerator": 1, "denominator": 0}')

assert divide_json(temp_path) is UNDEFINED


# ----------
# json.decoder.JSONDecodeError: try + finally
try:
    with open(temp_path, 'w') as f:
        f.write('{"numerator": 1 bad data')
    
    divide_json(temp_path)
except:
    logging.exception('Expected')
else:
    assert False


# ----------
# OSError: try + else + finally
# (simulated hard dis is full)
try:
    with open(temp_path, 'w') as f:
        f.write('{"numerator": 1, "denominator": 10}')
    DIE_IN_ELSE_BLOCK = True
    
    divide_json(temp_path)
except:
    logging.exception('Expected')
else:
    assert False