# 11/26/2021 MAIN

# IMPORT LIBRARIES
import machine
import time
import DS3231
import Davis
import SCD30
import gc
import XBee
import Bytes


# SETUP I2C, CO2, CLOCK
i2c = machine.I2C(1, freq=32000)  # DS3231 is 32kHz, SCD-30 is 50kHz, # ORIGINAL: 40kHz
scd = SCD30.SCD30(i2c, 0x61)
scd.set_measurement_interval(2)
scd.set_altitude_comp(1300)
scd.start_continous_measurement()
ds = DS3231.DS3231(i2c)
#ds.DateTime([2021, 10, 25, 3, 22, 25, 0]) # [Year, Month, Day, Weekday, Hour, Minute, Second]

# MISCELLANEOUS SETUPS
#BUTTON_Pin = machine.Pin("D3", machine.Pin.IN)
dir_offset = 0  # Specify the angular offset of the actual wind vane from true North.
Davis.MR()  # Reset Counter Chip
gc.collect()

# PRINT SETTINGS
print('')
print('Memory:      ', gc.mem_free())
print('SCD Interval:', scd.get_measurement_interval())
print('SCD Altitude:', scd.get_altitude_comp())
print('SCD Factor:  ', scd.get_forced_recalibration())
print('SCD Auto?    ', scd.get_automatic_recalibration())
print('')

# SETUP XBEE
#TARGET_NODE_ID = 'GreenGrove'

try:
    TARGET_NODE_ID = 'TH'
    device = XBee.find_device(TARGET_NODE_ID)
    addr64 = device['sender_eui64']
    button = 1
except:
    button = 0

# FINAL PREP
time.sleep(5)
true_ut = ds.UnixTime(*ds.DateTime())
print(true_ut)

while 1:
    # Collect Time and Wind Data
    ut = ds.UnixTime(*ds.DateTime())
    windDir = Davis.wd(dir_offset)
    windCyc = Davis.ws()
    #button = BUTTON_Pin.value()

    # Check If Unixtime is synchronized
    if ut == true_ut:
        sync = True
        true_ut += 3
    else:
        sync = False

    # Collect SCD30 Data and Print All Results
    if scd.get_status_ready() == 1:
        conc, temp, humid = scd.read_measurement()
        conc = int(conc)
        temp = int(temp)
    else:
        conc = 0
        temp = 0
        humid = 0

    row = ((ut, windCyc, windDir, conc, temp))
    print(row)
    #print(ut, windDir, windCyc, int(conc), int(temp))
    #print(ut, windDir, windCyc, int(conc), int(temp), gc.mem_free(), button, sync)

    # Transmit Data via XBee
    active = 1
    if button == 1 and active == 1:
        start = time.ticks_ms()
        bn = 1
        bs = 10
        #bu1, bu2, bu3, bu4 = Bytes.ut_to_byte(ut)
        bw1, bw2 = Bytes.wind_to_byte(windCyc, windDir)
        bc1, bc2 = Bytes.ppm_to_byte(conc)
        bt = Bytes.temp_to_byte(temp)

        #XBee.transmit(addr64, bytes([bn, bu1, bu2, bu3, bu4, bw1, bw2, bc1, bc2, bt]))
        XBee.transmit(addr64, bytes([bn, bs, bw1, bw2, bc1, bc2, bt]))
        end = time.ticks_ms()
        print(end-start)

    # Wait for 3 Seconds According to Unix time
    now_ut = ds.UnixTime(*ds.DateTime())
    while now_ut < ut + 3:
        now_ut = ds.UnixTime(*ds.DateTime())
        #print("     ", now_ut)
        time.sleep(0.1)
    # Reset
    gc.collect()

