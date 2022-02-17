'''
    Last updated: 2-12-2022
    Adriann Liceralde
    Wireless Sensor Network Project
'''

# ----- IMPORT LIBRARIES
import gc
import time
from machine import Pin, ADC, I2C
import rtc
import davis
import sensirion
import fram
import xbee
import network

# ----- NODE SPECIFIC SETTINGS
transmit_active = 1
dir_offset = 0  # Specify the angular offset of the actual wind vane from true North.
bn = network.get_node_id()

# ----- SETUP MODULES
i2c = I2C(1, freq=32000)  # DS3231 is 32kHz, SCD-30 is 50kHz, # ORIGINAL: 40kHz
scd = sensirion.SCD30(i2c, 0x61)
scd.set_measurement_interval(2)
scd.set_altitude_comp(1300)
scd.start_continous_measurement()
storage = fram.get_fram(i2c)
locator_byt = fram.get_locator(storage)
ds = rtc.DS3231(i2c)
#ds.DateTime([2022, 2, 15, 17, 1, 30])  # [Year, Month, Day, Hour, Minute, Second]
previous_ut = ds.UnixTime(*ds.DateTime())
time.sleep(1)
# 1642629612

# ----- CONNECT TO HUB
addr64, rec_online = network.connect()

# ----- PRINT SETTINGS
xbee.transmit(addr64,  bytes([111, 111, 111, 111, 111, 111, 111, 111]))

print('')
print('Memory:      ', gc.mem_free())
print('RF identifier', bn)
print('Firmware ver:', hex(xbee.atcmd("VR")))
print('Hardware ver:', hex(xbee.atcmd("HV")))
print('Hub Address: ', addr64)
print('Hub Connect: ', rec_online)
print('Transmit On: ', transmit_active)
print('SCD Interval:', scd.get_measurement_interval())
print('SCD Altitude:', scd.get_altitude_comp())
print('SCD Factor:  ', scd.get_forced_recalibration())
print('SCD Auto?    ', scd.get_automatic_recalibration())
print('')
print('------------------------------------------------------------------------------')
# ----- FINALIZATION
davis.MR()
# gc.collect()
# time.sleep(5)
# true_ut = ds.UnixTime(*ds.DateTime())

battery_pin = ADC("D0")
#D1 is reserved for SCL
wd_pin = ADC("D2")  # ANEM_DIR in schematic
led_pin = Pin("D3", mode=Pin.OUT, value=1)
#bit1 = Pin("D4", mode=Pin.IN)  # COUNT_0 in schematic
#bit2 = Pin("D5", mode=Pin.IN)  # COUNT_1 in schematic
#D6 is reserved for RTS
#bit3 = Pin("D7", mode=Pin.IN)  # COUNT_2 in schematic
#D8 is reserved for DTR
#bit4 = Pin("D9", mode=Pin.IN)  # COUNT_3 in schematic
button_pin = Pin("D10", mode=Pin.IN, pull=Pin.PULL_DOWN)
#D11 is reserved for SDA
#bit5 = Pin("D12", mode=Pin.IN)  # COUNT_4 in schematic
#D13 is reserved for DOUT
#D14 is reserved for DIN
#MR_pin = Pin("D15", mode=Pin.OUT)  # COUNT_RST in schematic
#bit8 = Pin("D16", mode=Pin.ALT)  # COUNT_7 in schematic
#bit6 = Pin("D17", mode=Pin.ALT)  # COUNT_5 in schematic
#bit7 = Pin("D18", mode=Pin.ALT)  # COUNT_6 in schematic
fram_wp = Pin("D19", mode=Pin.OUT)

counter = 0
while 1:
    led_pin.value(1)
    # Collect Time, Wind, and SCD30
    while 1:
        ut = ds.UnixTime(*ds.DateTime())
        if ut > previous_ut and ut < previous_ut+100:
            break
        else:
            print("----------------------------------------------------------------RTC SETBACK------------------------------------")
            time.sleep(0.1)


    conc, temp, humid = scd.getData()
    wind_dir = davis.wd(dir_offset)

    if conc == 0 and temp == 0 and humid == 0:
        xbee.transmit(addr64, bytes([0, 0, 0, 0, 0, 0, 0]))
    #wind_cyc = counter
    wind_cyc = davis.ws()

    #Collect Battery Level and Button State
    vcc = battery_pin.read()/4095*3.3*5
    vcc = round(vcc, 2)
    button_state = button_pin.value()

    # Check if Unix Time is synchronized
    # if ut == true_ut:
    #     sync = True
    #     true_ut += 3
    # else:
    #     sync = False

    data = [transmit_active, rec_online, ut, conc, temp, humid, wind_dir, wind_cyc, gc.mem_free(), button_state, vcc]
    for i in range(0, len(data)):
        if i == len(data) - 1:
            print(data[i])
        else:
            print(data[i], end=",")
    # print(data)
    # print(ut, windDir, windCyc, int(conc), int(temp), gc.mem_free(), button, sync)

    bu1, bu2, bu3, bu4 = network.ut_to_byte(ut)
    bw1, bw2 = network.wind_to_byte(wind_cyc, wind_dir)
    bc1, bc2 = network.ppm_to_byte(conc)
    bt = network.temp_to_byte(temp)

    #vvc = int(vcc*1000)
    #bb1 = vvc // 256
    #bb2 = vvc - bb1 * 256

    #data = bytes([bn, bu1, bu2, bu3, bu4, bw1, bw2, bc1, bc2, bt])
    #locator_byt = fram.emergency_storage(storage, locator_byt, data, previous_ut, include_unix=True)
    #data = bytes([bu1, bu2, bu3, bu4, bw1, bw2, bc1, bc2, bt, bb1, bb2])
    #locator_byt = fram.battery_storage(storage, locator_byt, data, previous_ut, include_unix=True)
    previous_ut = ut


    # Transmit to Hub
    if rec_online == 1 and transmit_active == 1:
        bu1, bu2, bu3, bu4 = network.ut_to_byte(ut)
        bw1, bw2 = network.wind_to_byte(wind_cyc, wind_dir)
        bc1, bc2 = network.ppm_to_byte(conc)
        bt = network.temp_to_byte(temp)

        try:
            # xbee.transmit(addr64, bytes([bn, 10, 20, 30, 40, 50, 60, 70, 80, 90]))
            xbee.transmit(addr64, bytes([bn, bu1, bu2, bu3, bu4, bw1, bw2, bc1, bc2, bt]))
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
    #
    # # Wait for 3 Seconds According to Unix time
    # # time.sleep(3)

    led_pin.value(0)
    now_ut = ds.UnixTime(*ds.DateTime())
    while now_ut < ut + 3:
        now_ut = ds.UnixTime(*ds.DateTime())
        # print(now_ut)
        time.sleep(0.1)
    gc.collect()
    counter += 1
    if counter == 255:
        counter = 0
