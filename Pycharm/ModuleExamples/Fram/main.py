# Laptop - 12/18/21

# https://github.com/peterhinch/micropython_eeprom
import fram_test
import time
from machine import Pin

WP = Pin("D19", Pin.OUT)
fram = fram_test.get_fram()

def full_clear():
    for i in range(1, 33):
        fram[1024*(i-1) : 1024*i] = b'\x00'*1024

#full_clear()

WP.value(0)
fram[0] = 20
fram[1] = 10
loc_byt = fram[0:2]
loc_int = int.from_bytes(loc_byt, "big")

# u1 u2 u3 u4
# bs w1 w2 c1 c2 t1