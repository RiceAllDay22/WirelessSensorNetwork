'''
    Last updated: 1-19-2022
    Adriann Liceralde
    Wireless Sensor Network Project
'''

# ----- IMPORT LIBRARIES
import gc
import time
import machine
import fram
import xbee
import network

i2c = machine.I2C(1, freq=32000)

# ----- NODE SPECIFIC SETTINGS
transmit_active = 0
dir_offset = 0  # Specify the angular offset of the actual wind vane from true North.
bn = network.get_node_id()

# ----- SETUP MODULES
i2c = machine.I2C(1, freq=32000)
storage = fram.get_fram(i2c)

# ----- CONNECT TO HUB
addr64, rec_online = network.connect()


# while 1:
#     if rec_online == 1 and transmit_active == 1:
#
#         try:
#             xbee.transmit(addr64, bytes([bn, 10, 20, 30, 40, 50, 60, 70, 80, 90]))
#             #xbee.transmit(addr64, bytes([bn, bu1, bu2, bu3, bu4, bw1, bw2, bc1, bc2, bt]))
#         except Exception as e:
#             rec_online = 0
#             print("Transmit failure: %s" % str(e))
#
#     elif rec_online == 0 and transmit_active == 1:
#         addr64, rec_online = network.connect()
#
#     elif transmit_active == 0:
#         print("Turned off")

def locator_reset():
    storage[0:2] = b'\x00\x02'
    return storage[0:2]

def get_locator():
    return storage[0:2]

locator_byt = locator_reset()
storage[0:20] = b'\x00'*20


previous_ut = 1642662590
now_ut = 1642662593


def emergency_storage(locator_byt, previous_ut, now_ut):
    # Get Data
    bs = now_ut - previous_ut
    bw1 = 111
    bw2 = 222
    bc1 = 100
    bc2 = 200
    bt = 50
    data = bytes([bs, bw1, bw2, bc1, bc2, bt])

    # Get FRAM Locator
    locator_int = int.from_bytes(locator_byt, "big")

    # Save Data to FRAM
    print(storage[locator_int:locator_int + 6])
    storage[locator_int:locator_int + 6] = data
    print(storage[locator_int:locator_int + 6])
    # print(locator_byt, locator_int, locator_byt[0] * 256 + locator_byt[1])

    # Update FRAM Locator
    locator_int = locator_int + 6
    locator_byt = locator_int.to_bytes(2, "big")
    storage[0:2] = locator_byt
    # print(locator_byt_new, locator_int_new, locator_byt_new[0]*256 + locator_byt_new[1])

    print(data)
    return locator_byt


# emergency_storage(locator_byt, previous_ut, now_ut)
