# IMPORT LIBRARIES
from machine import I2C, Pin
import gc
import DS3231
import SCD30
from Davis import wd, ws, MR
import time


# SETUP PINS AND MODULES
LED_pin = Pin("D10", Pin.OUT)
LED_pin.value(0)

i2c = I2C(1, freq = 30000)
scd = SCD30.SCD30(i2c, 0x61)
scd.set_measurement_interval(2)
ds = DS3231.DS3231(i2c)
#ds.DateTime([2021, 8, 7, 1, 16, 30, 0]) # [Year, Month, Day, Weekday, Hour, Minute, Second]



time.sleep(5)
# CALL MISCELLANEOUS FUNCTIONS AND SETUP VARIABLES
MR()
gc.collect()
print(gc.mem_free())

conc = 0
temp = 0
length = 1200


while 1:
    for i in range(0, 1200):
        # WIND
        windDir = wd()
        windCyc = ws()

        # GAS AND TEMP
        conc, temp = scd.get_scd()

        # TIME
        ut = ds.get_unixtime()
        print(ut, conc, temp, windDir, windCyc, gc.mem_free())

        # WAIT UNTIL NEXT MEASUREMENT
        LED_pin.value(0)

        #time.sleep(1)
        now_ut = ds.get_unixtime()
        while now_ut < ut + 3:
            #time.sleep(1)
            now_ut = ds.get_unixtime()

        LED_pin.value(1)
        gc.collect()


# co2 = None
#
# while 1:
#     try:
#         co2 = scd.read_measurement()
#         if co2[0] == co2[0]:
#             break
#     except:
#         print("Error Trying again...")

