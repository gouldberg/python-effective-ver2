#!/usr/bin/env PYTHONHASHSEED=1234 python3


# ------------------------------------------------------------------------------
# for + else:  else block is executed after for block
# ------------------------------------------------------------------------------

# else (not 'and') block is executed after for block
for i in range(3):
    print('Loop', i)
else:
    print('Else block!')


# -----------
# Surprisingly, even if for is not executed, else block is executed.
for x in []:
    print('Never runs')
else:
    print('For Else block!')


# ----------
# else block is NOT executed if for is break
for i in range(3):
    print('Loop', i)
    if i == 1:
        break
else:
    print('Else block!')


# ------------------------------------------------------------------------------
# while + else:  Also else block is executed after while is failed, ended
# ------------------------------------------------------------------------------

while False:
    print('Never runs')
else:
    print('While Else block!')


# ----------
i = 0
while i < 3:
    print('i : {i}')
    i += 1
else:
    print('While Else block!')


# ------------------------------------------------------------------------------
# for + else:  else block can be used for searching something in loop --> but recommended NOT to use for + else.
# Search coprime　（互いに素）
# ------------------------------------------------------------------------------

a = 4
b = 9

for i in range(2, min(a, b) + 1):
    print('Testing', i)
    if a % i == 0 and b % i == 0:
        print('Not coprime')
        break
else:
    # if a and b are coprime,
    # for is not break and else block is executed
    print('Coprime')


# ----------
def coprime(a, b):
    for i in range(2, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            return False
    return True

assert coprime(4, 9)
assert not coprime(3, 6)


# ------------------------------------------------------------------------------
# Not use else:
# Search coprime
# ------------------------------------------------------------------------------

def coprime_alternate(a, b):
    is_coprime = True
    for i in range(2, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            is_coprime = False
            break
    return is_coprime

assert coprime_alternate(4, 9)
assert not coprime_alternate(3, 6)
