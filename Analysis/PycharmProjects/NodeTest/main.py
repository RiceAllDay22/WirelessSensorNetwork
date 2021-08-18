# IMPORT LIBRARIES
from machine import I2C, Pin
import DS3231
import time


# SETUP PINS AND MODULES
LED_pin = Pin("D10", Pin.OUT)
LED_pin.value(0)

i2c = I2C(1, freq = 40000)
ds = DS3231.DS3231(i2c)
#ds.DateTime([2021, 8, 7, 1, 16, 30, 0]) # [Year, Month, Day, Weekday, Hour, Minute, Second]


while 1:
    LED_pin.value(1)
    time.sleep(0.5)
    LED_pin.value(0)
    
    # TIME
    #ut = ds.get_unixtime()

    dt = ds.DateTime()
    ut = ds.UnixTime(*dt)
    print(dt, ut)

    #unix = ds.get_unixtime()
    #print(dt, unix)
    time.sleep(0.5)


    #now_ut = ds.UnixTime(ds.DateTime())
    #while now_ut

    # WAIT UNTIL NEXT MEASUREMENT




