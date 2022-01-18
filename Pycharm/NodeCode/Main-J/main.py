# 11/30/2021 MAIN

transmit = 1
dir_offset = 0  # Specify the angular offset of the actual wind vane from true North.

# ----- IMPORT LIBRARIES
import machine
import time
import DS3231
import Davis
import SCD30
import gc
import XBee
import Bytes
import xbee #import Fram


# ----- RF NODE ID
NODE_ID = xbee.atcmd("NI")
if NODE_ID == 'PCB-XBee':
    bn = 1
elif NODE_ID == 'RyanBoard':
    bn = 2
else:
    bn = 111


# ----- SETUP MODULES
i2c = machine.I2C(1, freq=32000)  # DS3231 is 32kHz, SCD-30 is 50kHz, # ORIGINAL: 40kHz
scd = SCD30.SCD30(i2c, 0x61)
scd.set_measurement_interval(2)
scd.set_altitude_comp(1300)
scd.start_continous_measurement()
ds = DS3231.DS3231(i2c)# ds.DateTime([2021, 10, 25, 3, 22, 25, 0]) # [Year, Month, Day, Weekday, Hour, Minute, Second]#fram = Fram.FRAM(i2c)


# ----- CONNECT TO HUB
try:
    TARGET_NODE_ID = 'RedGrove'
    device = XBee.find_device(TARGET_NODE_ID)
    addr64 = device['sender_eui64']
    rec_online = 1
except:
    rec_online = 0


# ----- PRINT SETTINGS
print('')
print('Memory:      ', gc.mem_free())
print('RF identifier', NODE_ID)
print('Firmware ver:', hex(xbee.atcmd("VR")))
print('Hardware ver:', hex(xbee.atcmd("HV")))
print('Hub Connect: ',  rec_online)
print('SCD Interval:', scd.get_measurement_interval())
print('SCD Altitude:', scd.get_altitude_comp())
print('SCD Factor:  ', scd.get_forced_recalibration())
print('SCD Auto?    ', scd.get_automatic_recalibration())
print('')


# ----- FINALIZATION
gc.collect()
time.sleep(5)
Davis.MR()
true_ut = ds.UnixTime(*ds.DateTime())


while 1:
    # Collect Time and Wind Data
    ut = ds.UnixTime(*ds.DateTime())
    windDir = Davis.wd(dir_offset)
    windCyc = Davis.ws()

    # Check if Unix Time is synchronized
    if ut == true_ut:
        sync = True
        true_ut += 3
    else:
        sync = False

    # Collect SCD30 Data
    if scd.get_status_ready() == 1:
        conc, temp, humid = scd.read_measurement()
        conc = int(conc)
        temp = int(temp)
    else:
        conc, temp, humid = 0, 0, 0


    # Print Data
    row = ((ut, windCyc, windDir, conc, temp))
    print(row)
    # print(ut, windDir, windCyc, int(conc), int(temp))
    # print(ut, windDir, windCyc, int(conc), int(temp), gc.mem_free(), button, sync)

    # Transmit to Hub
    if rec_online == 1 and transmit == 1:
        start = time.ticks_ms()
        bu1, bu2, bu3, bu4 = Bytes.ut_to_byte(ut)
        bw1, bw2 = Bytes.wind_to_byte(windCyc, windDir)
        bc1, bc2 = Bytes.ppm_to_byte(conc)
        bt = Bytes.temp_to_byte(temp)

        try:
            XBee.transmit(addr64, bytes([bn, bu1, bu2, bu3, bu4, bw1, bw2, bc1, bc2, bt]))
        except Exception as e:
            print("Transmit failure: %s" % str(e))

        end = time.ticks_ms()
        print(end - start)

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
        time.sleep(0.5)

    # Reset
    gc.collect()