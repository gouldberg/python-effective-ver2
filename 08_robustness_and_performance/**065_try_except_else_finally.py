#!/usr/bin/env PYTHONHASHSEED=1234 python3

import logging

# ------------------------------------------------------------------------------
# finally:  always runs after try block
# ------------------------------------------------------------------------------

def try_finally_example(filename):
    print('* Opening file')
    handle = open(filename, encoding='utf-8') # May raise OSError
    try:
        print('* Reading data')
        return handle.read()  # May raise UnicodeDecodeError
    finally:
        print('* Calling close()')
        handle.close()        # Always runs after try block


try:
    filename = 'random_data.txt'
    
    with open(filename, 'wb') as f:
        f.write(b'\xf1\xf2\xf3\xf4\xf5')  # Invalid utf-8
    
    data = try_finally_example(filename)
    # This should not be reached.
    import sys
    sys.exit(1)
except:
    logging.exception('Expected')
else:
    assert False


# Example 3
try:
    try_finally_example('does_not_exist.txt')
except:
    logging.exception('Expected')
else:
    assert False


# Example 4
import json

def load_json_key(data, key):
    try:
        print('* Loading JSON data')
        result_dict = json.loads(data)  # May raise ValueError
    except ValueError as e:
        print('* Handling ValueError')
        raise KeyError(key) from e
    else:
        print('* Looking up key')
        return result_dict[key]         # May raise KeyError


# Example 5
assert load_json_key('{"foo": "bar"}', 'foo') == 'bar'


# Example 6
try:
    load_json_key('{"foo": bad payload', 'foo')
except:
    logging.exception('Expected')
else:
    assert False


# Example 7
try:
    load_json_key('{"foo": "bar"}', 'does not exist')
except:
    logging.exception('Expected')
else:
    assert False


# Example 8
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
        if DIE_IN_ELSE_BLOCK:
            import errno
            import os
            raise OSError(errno.ENOSPC, os.strerror(errno.ENOSPC))
        handle.write(result)    # May raise OSError
        return value
    finally:
        print('* Calling close()')
        handle.close()          # Always runs


# Example 9
temp_path = 'random_data.json'

with open(temp_path, 'w') as f:
    f.write('{"numerator": 1, "denominator": 10}')

assert divide_json(temp_path) == 0.1


# Example 10
with open(temp_path, 'w') as f:
    f.write('{"numerator": 1, "denominator": 0}')

assert divide_json(temp_path) is UNDEFINED


# Example 11
try:
    with open(temp_path, 'w') as f:
        f.write('{"numerator": 1 bad data')
    
    divide_json(temp_path)
except:
    logging.exception('Expected')
else:
    assert False


# Example 12
try:
    with open(temp_path, 'w') as f:
        f.write('{"numerator": 1, "denominator": 10}')
    DIE_IN_ELSE_BLOCK = True
    
    divide_json(temp_path)
except:
    logging.exception('Expected')
else:
    assert False