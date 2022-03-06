'''
    Last updated: 3-4-2022
    Adriann Liceralde
    Wireless Sensor Network Project
'''

# ----- IMPORT LIBRARIES
import gc
import time
from machine import Pin, I2C
import rtc
import network
import xbee

# ----- NODE SPECIFIC SETTINGS
transmit_active = 1
dir_offset = 0  # Specify the angular offset of the actual wind vane from true North.
bn = network.get_node_id()

# ----- SETUP MODULES
i2c = I2C(1, freq=32000)  # DS3231 is 32kHz, SCD-30 is 50kHz, # ORIGINAL: 40kHz
ds = rtc.DS3231(i2c)
previous_ut = ds.UnixTime(*ds.DateTime())
time.sleep(1)
counter = 0

# ----- SETUP PINS
button_pin = Pin("D4", Pin.IN)

# ----- CONNECT TO HUB
addr64, rec_online = network.connect()
xbee.transmit(addr64,  bytes([bn, 111, 111, 111, 111, 111, 111, 111, 111]))




# ----- MAIN LOOP
while 1:

    # Collect Time, Wind, and SCD30
    while 1:
        ut = ds.UnixTime(*ds.DateTime())
        if previous_ut < ut < previous_ut+50:
            break
        else:
            print(
                "----------------------------------------------------------------RTC SETBACK------------------------------------")
            time.sleep(0.1)
    conc, temp, humid = 1000, 30, 10
    wind_dir = 180
    wind_cyc = 0
    button_state = button_pin.value()
    vcc = 5

    # Print Data
    data = [transmit_active, rec_online, ut, conc, temp, humid, wind_dir, wind_cyc, gc.mem_free(), button_state, vcc]
    for i in range(0, len(data)):
        if i == len(data) - 1:
            print(data[i])
        else:
            print(data[i], end=",")

    # Convert to Bytes
    bu1, bu2, bu3, bu4 = network.ut_to_byte(ut)
    bw1, bw2 = network.wind_to_byte(wind_cyc, wind_dir)
    bc1, bc2 = network.ppm_to_byte(conc)
    bt = network.temp_to_byte(temp)
    previous_ut = ut

    # Transmit to Hub
    if rec_online == 1 and transmit_active == 1:
        bu1, bu2, bu3, bu4 = network.ut_to_byte(ut)
        bw1, bw2 = network.wind_to_byte(wind_cyc, wind_dir)
        bc1, bc2 = network.ppm_to_byte(conc)
        bt = network.temp_to_byte(temp)
        bv1 = vcc // 256
        bv2 = vcc - bv1 * 256

        try:
            # xbee.transmit(addr64, bytes([bn, 10, 20, 30, 40, 50, 60, 70, 80, 90]))
            xbee.transmit(addr64, bytes([bn, bu1, bu2, bu3, bu4, bw1, bw2, bc1, bc2, bt, bv1, bv2]))
        except Exception as e:
            rec_online = 0
            print("Transmit failure: %s" % str(e))

    elif rec_online == 0 and transmit_active == 1:
        addr64, rec_online = network.connect()

    # Check if there is an incoming broadcast
    received_msg = xbee.receive()
    if received_msg:
        sender = received_msg['sender_eui64']
        payload = received_msg['payload']
        print("Data received from %s >> %s" % (''.join('{:02x}'.format(x).upper() for x in sender),
                                               payload.decode()))

    # Wait for 3 Seconds According to Unix time
    now_ut = ds.UnixTime(*ds.DateTime())
    while now_ut < ut + 3:
        now_ut = ds.UnixTime(*ds.DateTime())
        # print(now_ut)
        time.sleep(0.1)
    gc.collect()
    counter += 1
    if counter == 255:
        counter = 0
