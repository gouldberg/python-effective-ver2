#!/usr/bin/env PYTHONHASHSEED=1234 python3

import os
import time
from datetime import datetime, timezone
import pytz


# ------------------------------------------------------------------------------
# time:
#   - time.localtime()
#   - time.strftime()
#   - time.strptime()
#   - time.mktime()
# ------------------------------------------------------------------------------

now = 1552774475

# convert UNIX time stamp (seconds from UTC UNIX epoch) to local time of host timezone
local_tuple = time.localtime(now)


# time.struct_time:  year, month, day, hour, min, sec, wday, yday, isdst
print(local_tuple)


# convert time.struct_time to readable
time_format = '%Y-%m-%d %H:%M:%S'
time_str = time.strftime(time_format, local_tuple)
print(time_str)


# convert string of time_format to time.struct_time
time_tuple = time.strptime(time_str, time_format)
print(time_tuple)


# convert time.struct_time to UNIX time stamp
utc_now = time.mktime(time_tuple)
print(utc_now)


# ------------------------------------------------------------------------------
# time module:
#   - platform dependent, not work appropriately for multiple local clocks.
#   - use only for conversion between UTC and host computer
#   - do not use conversion between local clocks.
# ------------------------------------------------------------------------------

# Try to convert to PDT timezone, but ValueError (not match format)

if os.name == 'nt':
    print("This example doesn't work on Windows")
else:
    parse_format = '%Y-%m-%d %H:%M:%S %Z'
    depart_sfo = '2019-03-16 15:45:16 PDT'
    time_tuple = time.strptime(depart_sfo, parse_format)
    time_str = time.strftime(time_format, time_tuple)
    print(time_str)

try:
    arrival_nyc = '2019-03-16 23:33:24 EDT'
    time_tuple = time.strptime(arrival_nyc, time_format)
except:
    logging.exception('Expected')
else:
    assert False


# ------------------------------------------------------------------------------
# datetime module
#   - datetime()
#   - datetime.replace()
#   - datetime.replace().astimezone()
#   - datetime.strptime()
#   - datetime.strptime().timetuple()
#   - time.mktime(datetime.strptime().timetuple())
#
# datetime module does have tzinfo class and time zone related computation,
# but does not provide other timezone definition
# ------------------------------------------------------------------------------

# ----------
# convert UTC to local time
now = datetime(2019, 3, 16, 22, 14, 35)
now_utc = now.replace(tzinfo=timezone.utc)
now_local = now_utc.astimezone()

now
now_utc
now_local

print(now)
print(now_utc)
print(now_local)


# ----------
# convert local time string to UTC clock
time_str = '2019-03-16 15:14:35'
now = datetime.strptime(time_str, time_format)

# time.struct_time
time_tuple = now.timetuple()
utc_now = time.mktime(time_tuple)

time_str
now
time_tuple
utc_now

print(utc_now)


# ------------------------------------------------------------------------------
# pytz
#   - include database of timezone
# ------------------------------------------------------------------------------

# ----------
# convert NY time to UTC time
arrival_nyc = '2019-03-16 23:33:24'
time_format = '%Y-%m-%d %H:%M:%S'

nyc_dt_naive = datetime.strptime(arrival_nyc, time_format)
eastern = pytz.timezone('US/Eastern')
nyc_dt = eastern.localize(nyc_dt_naive)
utc_dt = pytz.utc.normalize(nyc_dt.astimezone(pytz.utc))


nyc_dt_naive
eastern
nyc_dt
utc_dt

print(utc_dt)


# ----------
# UTC time (for given NY clock) to US/Pacific clock
pacific = pytz.timezone('US/Pacific')
sf_dt = pacific.normalize(utc_dt.astimezone(pacific))

pacific

nyc_dt
utc_dt
sf_dt

print(nyc_dt)
print(utc_dt)
print(sf_dt)


# ----------
# UTC time (for given NY clock) to Asia/Katmandu clock
nepal = pytz.timezone('Asia/Katmandu')
nepal_dt = nepal.normalize(utc_dt.astimezone(nepal))

nepal

nyc_dt
utc_dt
sf_dt
nepal_dt

print(nyc_dt)
print(utc_dt)
print(sf_dt)
print(nepal_dt)
