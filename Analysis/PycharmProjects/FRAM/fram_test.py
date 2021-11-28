# fram_test.py MicroPython test program for Adafruit FRAM devices.

# Released under the MIT License (MIT). See LICENSE.
# Copyright (c) 2019 Peter Hinch

import uos
import time
import machine
from fram_i2c import FRAM


i2c = machine.I2C(1, freq=32000)
# Return an FRAM array. Adapt for platforms other than Pyboard.
def get_fram():
    fram = FRAM(i2c)
    print('Instantiated FRAM')
    return fram

# Dumb file copy utility to help with managing FRAM contents at the REPL.
def cp(source, dest):
    if dest.endswith('/'):  # minimal way to allow
        dest = ''.join((dest, source.split('/')[-1]))  # cp /sd/file /fram/
    with open(source, 'rb') as infile:  # Caller should handle any OSError
        with open(dest,'wb') as outfile:  # e.g file not found
            while True:
                buf = infile.read(100)
                outfile.write(buf)
                if len(buf) < 100:
                    break

# ***** TEST OF DRIVER *****
def _testblock(eep, bs):
    d0 = b'this >'
    d1 = b'<is the boundary'
    d2 = d0 + d1
    garbage = b'xxxxxxxxxxxxxxxxxxx'
    start = bs - len(d0)
    end = start + len(garbage)
    eep[start : end] = garbage
    res = eep[start : end]
    if res != garbage:
        return 'Block test fail 1:' + str(list(res))
    end = start + len(d0)
    eep[start : end] = d0
    end = start + len(garbage)
    res = eep[start : end]
    if res != b'this >xxxxxxxxxxxxx':
        return 'Block test fail 2:' + str(list(res))
    start = bs
    end = bs + len(d1)
    eep[start : end] = d1
    start = bs - len(d0)
    end = start + len(d2)
    res = eep[start : end]
    if res != d2:
        return 'Block test fail 3:' + str(list(res))

def test():
    fram = get_fram()
    sa = 1000
    for v in range(256):
        fram[sa + v] = v
    for v in range(256):
        if fram[sa + v] != v:
            print('Fail at address {} data {} should be {}'.format(sa + v, fram[sa + v], v))
            break
    else:
        print('Test of byte addressing passed')
    data = uos.urandom(30)
    sa = 2000
    fram[sa:sa + 30] = data
    if fram[sa:sa + 30] == data:
        print('Test of slice readback passed')
    # On FRAM the only meaningful block test is on a chip boundary.
    block = fram._c_bytes
    if fram._a_bytes > block:
        res = _testblock(fram, block)
        if res is None:
            print('Test chip boundary {} passed'.format(block))
        else:
            print('Test chip boundary {} fail'.format(block))
            print(res)
    else:
        print('Test chip boundary skipped: only one chip!')



# ***** TEST OF HARDWARE *****
def full_test():
    fram = get_fram()
    page = 0
    for sa in range(0, len(fram), 256):
        data = uos.urandom(256)
        fram[sa:sa + 256] = data
        if fram[sa:sa + 256] == data:
            print('Page {} passed'.format(page))
        else:
            print('Page {} readback failed.'.format(page))
        page += 1