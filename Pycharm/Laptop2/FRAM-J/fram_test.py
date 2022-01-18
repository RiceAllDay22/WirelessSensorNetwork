# https://github.com/peterhinch/micropython_eeprom

# fram_test.py MicroPython test program for Adafruit FRAM devices.

# Released under the MIT License (MIT). See LICENSE.
# Copyright (c) 2019 Peter Hinch

import uos
import time
import machine
from fram_i2c import FRAM

# Raspberry Pico
#sda = machine.Pin(8)
#scl = machine.Pin(9)
#i2c = machine.I2C(0, sda=sda, scl=scl, freq=32000)


i2c = machine.I2C(1, freq=32000)

# Return an FRAM array. Adapt for platforms other than Pyboard.
def get_fram():
    fram = FRAM(i2c)
    print('Instantiated FRAM')
    return fram


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


# ***** TEST OF HARDWARE *****
def full_test():
    fram = get_fram()
    page = 0
    for sa in range(0, len(fram), 256):
        data = uos.urandom(256)
        fram[sa:sa + 256] = data
        if fram[sa:sa + 256] == data:
            pass
            #print('Page {} passed'.format(page))
        else:
            print('Page {} readback failed.'.format(page))
        page += 1
    print('Complete')