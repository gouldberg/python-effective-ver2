#!/usr/bin/env PYTHONHASHSEED=1234 python3

# Enable these lines to make this example work on Windows
# import os
# os.environ['COMSPEC'] = 'powershell'

import os
import subprocess
import time


# ------------------------------------------------------------------------------
# subprocess
# ------------------------------------------------------------------------------

# subprocess is executed independent to Python

# subprocess run
# run does all:  execute process, read, stop ...
result = subprocess.run(
    ['echo', 'Hello from the child!'],
    capture_output=True,
    # Enable this line to make this example work on Windows
    # shell=True,
    encoding='utf-8')


print(result)

# check return code:  No exception means it exited cleanly
result.check_returncode()

print(result.stdout)


# ------------------------------------------------------------------------------
# Popen
# to check by polling periodically while Python do some else.
# ------------------------------------------------------------------------------

# Use this line instead to make this example work on Windows
# proc = subprocess.Popen(['sleep', '1'], shell=True)

proc = subprocess.Popen(['sleep', '1'])

print(proc)

# while python do something, proc.poll check child process
while proc.poll() is None:
    print('Working...')
    # ----------
    # Some time-consuming work here
    import time
    time.sleep(0.3)
    # ----------

print('Exit status', proc.poll())


# ------------------------------------------------------------------------------
# communicate method to wait for child process to finish I/O
# ------------------------------------------------------------------------------

start = time.time()

sleep_procs = []

for _ in range(10):
    # Use this line instead to make this example work on Windows
    # proc = subprocess.Popen(['sleep', '1'], shell=True)
    proc = subprocess.Popen(['sleep', '1'])
    sleep_procs.append(proc)

# wait for child processes to finish I/O
for proc in sleep_procs:
    proc.communicate()

end = time.time()
delta = end - start

# It does not take less than 10 (= 1 * 10) seconds.
print(f'Finished in {delta:.3} seconds')


# ------------------------------------------------------------------------------
# use command line arguments and I/O pipe
#   this script does some encryption
# ------------------------------------------------------------------------------

# On Windows, after installing OpenSSL, you may need to
# alias it in your PowerShell path with a command like:
# $env:path = $env:path + ";C:\Program Files\OpenSSL-Win64\bin"

def run_encrypt(data):
    env = os.environ.copy()
    env['password'] = 'zf7ShyBhZOraQDdE/FiZpm/m/8f9X+M1'
    # ----------
    # start child process by command lise arguments and I/O pipe
    proc = subprocess.Popen(
        ['openssl', 'enc', '-des3', '-pass', 'env:password'],
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)
    proc.stdin.write(data)
    proc.stdin.flush()  # Ensure that the child gets input
    return proc

procs = []

for _ in range(3):
    data = os.urandom(10)
    proc = run_encrypt(data)
    procs.append(proc)


for proc in procs:
    out, _ = proc.communicate()
    print(out[-10:])


# ------------------------------------------------------------------------------
# generate hash
# ------------------------------------------------------------------------------

# return subprocess.Popen

def run_hash(input_stdin):
    return subprocess.Popen(
        ['openssl', 'dgst', '-whirlpool', '-binary'],
        stdin=input_stdin,
        stdout=subprocess.PIPE)


encrypt_procs = []

hash_procs = []

for _ in range(3):
    data = os.urandom(100)
    encrypt_proc = run_encrypt(data)
    encrypt_procs.append(encrypt_proc)
    hash_proc = run_hash(encrypt_proc.stdout)
    hash_procs.append(hash_proc)

    # Ensure that the child consumes the input stream and the communicate() method doesn't inadvertently steal
    # input from the child. 
    # Also lets SIGPIPE propagate to the upstream process if the downstream process dies.
    encrypt_proc.stdout.close()
    encrypt_proc.stdout = None


for proc in encrypt_procs:
    proc.communicate()
    assert proc.returncode == 0


for proc in hash_procs:
    out, _ = proc.communicate()
    print(out[-10:])
    assert proc.returncode == 0


# ------------------------------------------------------------------------------
# Use timeout in communicate method,
# if you care about the case where child process does not respond in specified time, want to avoid some deadlocks,
# If not, raise subprocess.TimeoutExpired.
# ------------------------------------------------------------------------------

# Use this line instead to make this example work on Windows
# proc = subprocess.Popen(['sleep', '10'], shell=True)

proc = subprocess.Popen(['sleep', '10'])

try:
    proc.communicate(timeout=0.1)
except subprocess.TimeoutExpired:
    proc.terminate()
    proc.wait()

print('Exit status', proc.poll())
