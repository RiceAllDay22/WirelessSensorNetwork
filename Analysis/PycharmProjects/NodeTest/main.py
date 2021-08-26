# IMPORT LIBRARIES
from machine import I2C, Pin
import DS3231
import time
# import SCD30
# from Davis import MR, ws, wd

# SETUP PINS AND MODULES
i2c = I2C(1, freq = 40000)
#scd = SCD30.SCD30(i2c, 0x61)
#scd.set_measurement_interval(2)
ds = DS3231.DS3231(i2c)
#ds.DateTime([2021, 8, 7, 1, 16, 30, 0]) # [Year, Month, Day, Weekday, Hour, Minute, Second]


#MR()

while 1:
    dt = ds.DateTime()
    ut = ds.UnixTime(*dt)

    print(dt, ut)
    time.sleep(1)

    #LED_pin.value(1)
    #time.sleep(1)
    #LED_pin.value(0)
    
    # TIME
    #ut = ds.get_unixtime()

    #conc, temp = scd.get_scd()
    #indDir = wd()
    #windCyc = ws()


    #unix = ds.get_unixtime()
    #print(dt, unix)
    #time.sleep(0.5)


    #now_ut = ds.UnixTime(ds.DateTime())
    #while now_ut

    # WAIT UNTIL NEXT MEASUREMENT




