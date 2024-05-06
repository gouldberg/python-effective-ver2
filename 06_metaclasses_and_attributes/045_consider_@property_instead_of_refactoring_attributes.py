#!/usr/bin/env PYTHONHASHSEED=1234 python3

from datetime import datetime, timedelta


# ------------------------------------------------------------------------------
# Bucket example
# ------------------------------------------------------------------------------

class Bucket:
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.quota = 0

    def __repr__(self):
        return f'Bucket(quota={self.quota})'


def fill(bucket, amount):
    now = datetime.now()
    if (now - bucket.reset_time) > bucket.period_delta:
        bucket.quota = 0
        bucket.reset_time = now
    bucket.quota += amount


def deduct(bucket, amount):
    now = datetime.now()
    if (now - bucket.reset_time) > bucket.period_delta:
        return False  # Bucket hasn't been filled this period
    if bucket.quota - amount < 0:
        return False  # Bucket was filled, but not enough
    bucket.quota -= amount
    return True       # Bucket had enough, quota consumed


bucket = Bucket(60)
fill(bucket, 100)
print(bucket)


if deduct(bucket, 99):
    print('Had 99 quota')
else:
    print('Not enough for 99 quota')

print(bucket)


if deduct(bucket, 3):
    print('Had 3 quota')
else:
    print('Not enough for 3 quota')

print(bucket)


# ------------------------------------------------------------------------------
# NewBucket class with
#   getter and setter for quota
#   @property is helpful to improve to better model
# ------------------------------------------------------------------------------

class NewBucket:
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.max_quota = 0
        self.quota_consumed = 0

    def __repr__(self):
        return (f'NewBucket(max_quota={self.max_quota}, '
                f'quota_consumed={self.quota_consumed})')

    @property
    def quota(self):
        return self.max_quota - self.quota_consumed

    @quota.setter
    def quota(self, amount):
        delta = self.max_quota - amount
        if amount == 0:
            # Quota being reset for a new period
            self.quota_consumed = 0
            self.max_quota = 0
        elif delta < 0:
            # Quota being filled during the period
            self.max_quota = amount + self.quota_consumed
        else:
            # Quota being consumed during the period
            self.quota_consumed = delta


bucket = NewBucket(60)
print('Initial', bucket)


fill(bucket, 100)
print('Filled', bucket)


if deduct(bucket, 99):
    print('Had 99 quota')
else:
    print('Not enough for 99 quota')

print('Now', bucket)


if deduct(bucket, 3):
    print('Had 3 quota')
else:
    print('Not enough for 3 quota')

print('Still', bucket)


# ----------
bucket = NewBucket(6000)
assert bucket.max_quota == 0
assert bucket.quota_consumed == 0
assert bucket.quota == 0

fill(bucket, 100)
assert bucket.max_quota == 100
assert bucket.quota_consumed == 0
assert bucket.quota == 100

assert deduct(bucket, 10)
assert bucket.max_quota == 100
assert bucket.quota_consumed == 10
assert bucket.quota == 90

assert deduct(bucket, 20)
assert bucket.max_quota == 100
assert bucket.quota_consumed == 30
assert bucket.quota == 70

fill(bucket, 50)
assert bucket.max_quota == 150
assert bucket.quota_consumed == 30
assert bucket.quota == 120

assert deduct(bucket, 40)
assert bucket.max_quota == 150
assert bucket.quota_consumed == 70
assert bucket.quota == 80

assert not deduct(bucket, 81)
assert bucket.max_quota == 150
assert bucket.quota_consumed == 70
assert bucket.quota == 80

bucket.reset_time += bucket.period_delta - timedelta(1)
assert bucket.quota == 80
assert not deduct(bucket, 79)

fill(bucket, 1)
assert bucket.quota == 1
