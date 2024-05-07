#!/usr/bin/env PYTHONHASHSEED=1234 python3

import os
import timeit


# ------------------------------------------------------------------------------
# Client side (pseudo code) 
# ------------------------------------------------------------------------------

def timecode_to_index(video_id, timecode):
    return 1234
    # Returns the byte offset in the video data


def request_chunk(video_id, byte_offset, size):
    pass
    # Returns size bytes of video_id's data from the offset


video_id = ...

timecode = '01:09:14:28'

# 1234 for now
byte_offset = timecode_to_index(video_id, timecode)

# chunk size request: 20MB
size = 20 * 1024 * 1024

video_data = request_chunk(video_id, byte_offset, size)


# ------------------------------------------------------------------------------
# Server side
# only for
#   - get chunks from vide data cached in memory
#   - send user via socket
# ------------------------------------------------------------------------------

class NullSocket:
    def __init__(self):
        self.handle = open(os.devnull, 'wb')

    def send(self, data):
        self.handle.write(data)

# socket connection to client
socket = NullSocket()

# bytes containing data for video_id (bytes instance)
video_data = 100 * os.urandom(1024 * 1024)

# requested starting position
byte_offset = 1234
# requested chunk size: 20MB
size = 20 * 1024 * 1024

# slice bytes instance to chunk
# The problem is:
#   slicing bytes instance will produce data copy and consume CPU time
chunk = video_data[byte_offset:byte_offset + size]

socket.send(chunk)


# ----------
def run_test():
    chunk = video_data[byte_offset:byte_offset + size]
    # Call socket.send(chunk), but ignoring for benchmark

result = timeit.timeit(
    stmt='run_test()',
    globals=globals(),
    number=100) / 100

# 0.002 sec
# upper limit of server total throughput is 20 MB / 0.002 sec = 9.77 GB/secs
# upper limit of parallel of 500 clients = 1 CPU sec / 0.002 sec (not critical issue)
print(f'{result:0.9f} seconds')


# ------------------------------------------------------------------------------
# memoryview  (with buffer protocol)
#    buffer protocol is low-level C API
#    enable to access to data buffer (such as bytes instance)
# ------------------------------------------------------------------------------

data = b'shave and a haircut, two bits'

view = memoryview(data)

chunk = view[12:19]
print(chunk)

print('Size:           ', chunk.nbytes)
print('Data in view:   ', chunk.tobytes())

print('Underlying data:', chunk.obj)


# ------------------------------------------------------------------------------
# use memoryview to improve speed
# ------------------------------------------------------------------------------

video_view = memoryview(video_data)

def run_test():
    chunk = video_view[byte_offset:byte_offset + size]
    # Call socket.send(chunk), but ignoring for benchmark

result = timeit.timeit(
    stmt='run_test()',
    globals=globals(),
    number=100) / 100


# 0.000000656 secs.
# now the program is not in CPU constraint
# but in constraint of socket communication 
print(f'{result:0.9f} seconds')


# ------------------------------------------------------------------------------
# Client send vide stream to broadcast to other users.
# Server is required to read those new vide stream.
# ------------------------------------------------------------------------------

class FakeSocket:

    def recv(self, size):
        return video_view[byte_offset:byte_offset+size]

    def recv_into(self, buffer):
        source_data = video_view[byte_offset:byte_offset+size]
        buffer[:] = source_data

# socket connection to the client
socket = FakeSocket()
# cache of incoming video stream
video_cache = video_data[:]
# incoming buffer position
byte_offset = 1234

# incoming chunk size: 1MB
size = 1024 * 1024
chunk = socket.recv(size)

# memoryview
video_view = memoryview(video_cache)

before = video_view[:byte_offset]
after = video_view[byte_offset + size:]

new_cache = b''.join([before, chunk, after])

def run_test():
    # socket.recv return bytes instance
    chunk = socket.recv(size)
    before = video_view[:byte_offset]
    after = video_view[byte_offset + size:]
    new_cache = b''.join([before, chunk, after])

result = timeit.timeit(
    stmt='run_test()',
    globals=globals(),
    number=100) / 100

# 0.067 sec.
# receiving throughput:  14.9 MB/sec (= 1 MB / 0.067 sec)
# parallel client streaming video:  15 (= 14.9 / 1)
print(f'{result:0.9f} seconds')

# --> This program does not scale well ...


# ------------------------------------------------------------------------------
# bytearray is mutable version of bytes
# bytearray can be wrapped by memoryview (zero-copy)
# ------------------------------------------------------------------------------

my_bytes = b'hello'

# TypeError
# bytes instance is read only and can not be updated by index
my_bytes[0] = b'\x79'


# ----------
# bytearray is mutable version of bytes
my_array = bytearray(b'hello')
my_array[0] = 0x79
print(my_array)


# ----------
# bytearray wrapped by memoryview
my_array = bytearray(b'row, row, row your boat')
my_view = memoryview(my_array)
write_view = my_view[3:13]
write_view[:] = b'-10 bytes-'

# bytearray is updated (zero-copy)
print(my_array)


# ----------
# socket.recv_info, RawIOBase.readinto uses buffer protocol to data receiving, read.
video_array = bytearray(video_cache)
write_view = memoryview(video_array)

# slicing without copy !!
chunk = write_view[byte_offset:byte_offset + size]
socket.recv_into(chunk)


# ------------------------------------------------------------------------------
# bytearray is mutable version of bytes
# bytearray can be wrapped by memoryview
# ------------------------------------------------------------------------------

# socket connection to the client
socket = FakeSocket()
# cache of incoming video stream
video_cache = video_data[:]
# incoming buffer position
byte_offset = 1234

# incoming chunk size: 1MB
size = 1024 * 1024
chunk = socket.recv(size)


video_array = bytearray(video_cache)
write_view = memoryview(video_array)
chunk = write_view[byte_offset:byte_offset + size]
socket.recv_into(chunk)

def run_test():
    chunk = write_view[byte_offset:byte_offset + size]
    socket.recv_into(chunk)

result = timeit.timeit(
    stmt='run_test()',
    globals=globals(),
    number=100) / 100


# 0.0000735 sec
print(f'{result:0.9f} seconds')
