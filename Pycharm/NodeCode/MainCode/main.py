'''
    Last updated: 1-19-2022
    Adriann Liceralde
    Wireless Sensor Network Project
'''

# ----- IMPORT LIBRARIES
import gc
import time
import machine
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
i2c = machine.I2C(1, freq=32000)  # DS3231 is 32kHz, SCD-30 is 50kHz, # ORIGINAL: 40kHz
scd = sensirion.SCD30(i2c, 0x61)
scd.set_measurement_interval(2)
scd.set_altitude_comp(1300)
scd.start_continous_measurement()
storage = fram.get_fram(i2c)
ds = rtc.DS3231(i2c)
# ds.DateTime([2022, 1, 19, 22, 0, 0]) # [Year, Month, Day, Hour, Minute, Second]


# ----- CONNECT TO HUB
addr64, rec_online = network.connect()

# ----- PRINT SETTINGS
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

# ----- FINALIZATION
davis.MR()
# gc.collect()
# time.sleep(5)
# true_ut = ds.UnixTime(*ds.DateTime())


while 1:
    # Collect Time and Wind Data
    ut = ds.UnixTime(*ds.DateTime())
    wind_dir = davis.wd(dir_offset)
    wind_cyc = davis.ws()

    # Check if Unix Time is synchronized
    # if ut == true_ut:
    #     sync = True
    #     true_ut += 3
    # else:
    #     sync = False

    # Collect SCD30 Data
    if scd.get_status_ready() == 1:
        conc, temp, humid = scd.read_measurement()
        conc = int(conc)
        temp = int(temp)
    else:
        conc, temp, humid = 0, 0, 0
    print(rec_online, ut, conc, temp, humid, wind_dir, wind_cyc, gc.mem_free())
    # print(ut, windDir, windCyc, int(conc), int(temp), gc.mem_free(), button, sync)


    # Transmit to Hub
    if rec_online == 1 and transmit_active == 1:
        bu1, bu2, bu3, bu4 = network.ut_to_byte(ut)
        bw1, bw2 = network.wind_to_byte(wind_cyc, wind_dir)
        bc1, bc2 = network.ppm_to_byte(conc)
        bt = network.temp_to_byte(temp)

        try:
            #xbee.transmit(addr64, bytes([bn, 10, 20, 30, 40, 50, 60, 70, 80, 90]))
            xbee.transmit(addr64, bytes([bn, bu1, bu2, bu3, bu4, bw1, bw2, bc1, bc2, bt]))
        except Exception as e:
            rec_online = 0
            print("Transmit failure: %s" % str(e))

    elif rec_online == 0 and transmit_active == 1:
        addr64, rec_online = network.connect()

    #Check if there is an incoming broadcast
    received_msg = xbee.receive()
    if received_msg:
        sender = received_msg['sender_eui64']
        payload = received_msg['payload']
        print("Data received from %s >> %s" % (''.join('{:02x}'.format(x).upper() for x in sender),
                                               payload.decode()))


    # Wait for 3 Seconds According to Unix time
    # time.sleep(3)

    now_ut = ds.UnixTime(*ds.DateTime())
    while now_ut < ut + 3:
        now_ut = ds.UnixTime(*ds.DateTime())
        time.sleep(0.5)

    gc.collect()
