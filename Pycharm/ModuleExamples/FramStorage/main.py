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
import rtc


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
        print('ut:', ut)

        data = bytes([bn, bu1, bu2, bu3, bu4, bw1, bw2, bc1, bc2, bt])
        print(data)
        previous_ut = ut

        # Send to Hub
        if rec_online == 1 and transmit_active == 1:
            print("Send to Hub")
            try:
                xbee.transmit(addr64, data)

            except Exception as e:
                rec_online = 0
                print("Transmit failure: %s" % str(e))

        # Save to Fram
        if rec_online == 0 and transmit_active == 1:
            print("Save to Fram")
            locator_byt = fram.get_locator(storage)
            locator_byt = fram.emergency_storage(storage, locator_byt, data, previous_ut)
            addr64, rec_online = network.connect()
            print(addr64, rec_online)

        if transmit_active == 0:
            print("Turned off")

        time.sleep(2)

finally:
    print('End Code')
    print(data)



