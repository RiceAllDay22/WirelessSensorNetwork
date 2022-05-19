'''
    Last updated: 4-21-2022
    Adriann Liceralde
    Wireless Sensor Network Project
'''

# ----- IMPORT LIBRARIES
from machine import Pin, ADC, I2C, WDT, SOFT_RESET
import gc
import time
import rtc
import davis
import sensirion
import fram
import xbee
import network

# ----- NODE SPECIFIC SETTINGS
transmit_active = 1  # 0 = transmission to CentralHub is off. 1 = transmission is on.
dir_offset = 0  # Specify the angular offset of the actual wind vane from true North (0 to 359)
bn = network.get_node_id()  # Retrieve the node number of this RF module

# ----- SETUP MODULES
i2c = I2C(1, freq=32000)  # DS3231 is 32kHz, SCD-30 is 50kHz, # ORIGINAL: 40kHz
#scd = sensirion.SCD30(i2c, 0x61)
#scd.set_measurement_interval(2)
#scd.set_altitude_comp(1300)
#scd.start_continous_measurement()
storage = fram.get_fram(i2c)
locator_byt = fram.get_locator(storage)
locator_int = int.from_bytes(locator_byt, "big")
ds = rtc.DS3231(i2c)
# ds.DateTime([2022, 4, 15, 23, 0, 0])  # [Year, Month, Day, Hour, Minute, Second]

# ----- SETUP PINS
battery_pin = ADC("D0")
led_pin = Pin("D3", mode=Pin.OUT, value=1)
button_pin = Pin("D10", mode=Pin.IN, pull=Pin.PULL_DOWN)
fram_wp = Pin("D19", mode=Pin.OUT)

# ----- CONNECT TO HUB
addr64, rec_online = network.connect()
# xbee.transmit(addr64,  bytes([111, 111, 111, 111, 111, 111, 111, 111]))

# ----- PRINT SETTINGS
print('')
print('Free Memory: ', gc.mem_free())
print('RF identifier', bn)
print('Firmware ver:', hex(xbee.atcmd("VR")))
print('Hardware ver:', hex(xbee.atcmd("HV")))
print('Hub Address: ', addr64)
print('Hub Connect: ', rec_online)
print('Transmit On: ', transmit_active)
#print('SCD Interval:', scd.get_measurement_interval())
#print('SCD Altitude:', scd.get_altitude_comp())
#print('SCD Factor:  ', scd.get_forced_recalibration())
#print('SCD Auto?    ', scd.get_automatic_recalibration())
print('')
print('------------------------------------------------------------------------------')

# ----- FINALIZATION
# gc.collect()
# time.sleep(5)
davis.MR()
if locator_int > 2:
    fram.emergency_retrieve(storage, addr64, bn)
    locator_byt = storage[0:2]

#previous_ut = ds.get_unixtime()

#dog = WDT(timeout=60000, response=SOFT_RESET)

# ----- MAIN LOOP
while 1:
    led_pin.value(1)

    # Collect Time, Wind, and SCD30 data
    ut = ds.get_unixtime()
    conc, temp, humid = 400, 20, 20 # For testing purposes when SCD30 is disconnected
    #conc, temp, humid = scd.getData()
    wind_dir = davis.wd(dir_offset)
    if conc == 0 and temp == 0 and humid == 0:
        xbee.transmit(addr64, bytes([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
    wind_cyc = davis.ws()

    # Collect Battery Level and Button State
    vcc = battery_pin.read()
    vcc = vcc / 4095 * 3.3 * 5
    button_state = button_pin.value()

    # Print Data
    full_data = [transmit_active, rec_online, ut, conc, temp, humid, wind_cyc, wind_dir, gc.mem_free(), button_state, vcc]
    print(full_data)

    # Convert Data from Integers to Bytes
    bu1, bu2, bu3, bu4 = network.ut_to_byte(ut)
    bc1, bc2 = network.ppm_to_byte(conc)
    bwd, bt = network.windtemp_to_byte(wind_dir, temp)
    bws = wind_cyc
    data = [bn, bu1, bu2, bu3, bu4, bc1, bc2, bws, bwd, bt]

    # Transmit to Hub
    if rec_online == 1 and transmit_active == 1:
        try:
            xbee.transmit(addr64, bytes(data))
        except Exception as e:
            rec_online = 0
            print("Transmit failure: %s" % str(e))

    # Emergency Fram storage if  connection to Hub is lost
    elif rec_online == 0 and transmit_active == 1:
        locator_byt = fram.emergency_storage(storage, locator_byt, data)
        addr64, rec_online = network.connect()
        if rec_online == 1:
            fram.emergency_retrieve(storage, addr64, bn)

    # Check if there is an incoming broadcast
    received_msg = xbee.receive()
    if received_msg:
        print("Incoming broadcast from Central Hub:")
        sender = received_msg['sender_eui64']
        payload = received_msg['payload']
        b = payload

        # Check if incoming data is a Time Sync from CentralHub
        if len(b) == 8:
            print("Time Sync to %s-%s-%s %s:%s:%s" % (
                payload[1] + 2000, payload[2], payload[3], payload[4], payload[5], payload[6]))
            ds.DateTime([payload[1] + 2000, payload[2], payload[3], payload[4], payload[5], payload[6]])

    # Wait for 3 Seconds According to Unix time
    led_pin.value(0)
    now_ut = ds.UnixTime(*ds.DateTime())
    while now_ut < ut + 3:
        now_ut = ds.UnixTime(*ds.DateTime())
        time.sleep(0.1)
    gc.collect()

    #dog.feed()





# JUNK CODE

#Check for RTC Setback Error
# previous_ut = ds.UnixTime(*ds.DateTime())

    # while 1:
    #     ut = ds.UnixTime(*ds.DateTime())
    #     if ut > previous_ut and ut < previous_ut + 100:
    #         break
    #     else:
    #         print("----------------------------------------------------------------RTC SETBACK------------------------------------")
    #         time.sleep(0.1)

# previous_ut = ut



#Check unixtime sync with true_ut
# true_ut = ds.UnixTime(*ds.DateTime())
    # Check if Unix Time is synchronized
    # if ut == true_ut:
    #     sync = True
    #     true_ut += 3
    # else:
    #     sync = False