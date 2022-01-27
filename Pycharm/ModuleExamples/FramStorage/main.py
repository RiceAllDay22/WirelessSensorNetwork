'''
    Last updated: 1-19-2022
    Adriann Liceralde
    Wireless Sensor Network Project
'''

# ----- IMPORT LIBRARIES
import gc
print('After gc:', gc.mem_free())
import time
print('After time:', gc.mem_free())
import machine
print('After machine:', gc.mem_free())
import xbee
print('After xbee:', gc.mem_free())
import fram
print('After fram:', gc.mem_free())
import network
print('After network:', gc.mem_free())
import rtc
print('After rtc:', gc.mem_free())

# ----- NODE SPECIFIC SETTINGS
transmit_active = 1
dir_offset = 0  # Specify the angular offset of the actual wind vane from true North.
bn = network.get_node_id()

# ----- SETUP MODULES
i2c = machine.I2C(1, freq=32000)
storage = fram.get_fram(i2c)
locator_byt = fram.get_locator(storage)
ds = rtc.DS3231(i2c)

# ----- CONNECT TO HUB
addr64, rec_online = network.connect()

ds.DateTime([2020, 9, 13, 12, 26, 40])
previous_ut = ds.UnixTime(*ds.DateTime())
time.sleep(1)

try:
    while 1:
        # Get Data
        ut = ds.UnixTime(*ds.DateTime())
        bu1, bu2, bu3, bu4 = network.ut_to_byte(ut)
        bw1, bw2 = 111, 222
        bc1, bc2 = 100, 200
        bt = 50

        data = bytes([bn, bu1, bu2, bu3, bu4, bw1, bw2, bc1, bc2, bt])
        print(ut, bw1, bw2, bc1, bc2, bt)

        # Send to Hub
        if rec_online == 1 and transmit_active == 1:
            try:
                xbee.transmit(addr64, data)
                print("^ Sent to Hub")

            except Exception as e:
                print("^ Transmit failure: %s" % str(e))
                rec_online = 0
                previous_ut = ut
                locator_byt = fram.get_locator(storage)
                locator_byt = fram.emergency_storage(storage, locator_byt, data, previous_ut, include_unix=True)
                print("^ Save to Fram")

        # Save to Fram
        elif rec_online == 0 and transmit_active == 1:
            print("^ Saved to Fram")
            locator_byt = fram.get_locator(storage)
            locator_byt = fram.emergency_storage(storage, locator_byt, data, previous_ut, include_unix=False)
            addr64, rec_online = network.connect()
            #print(addr64, rec_online)

        elif transmit_active == 0:
            print("Turned off")

        previous_ut = ut
        time.sleep(3)

finally:
    print('End Code')
    print(data)



