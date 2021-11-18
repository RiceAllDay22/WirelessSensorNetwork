import machine
import DS3231
import time

i2c = machine.I2C(1, freq=32000)  # DS3231 is 32kHz, SCD-30 is 50kHz, # ORIGINAL: 40kHz
ds = DS3231.DS3231(i2c)
#ds.DateTime([2021, 11, 13, 1, 7, 22, 50]) # [Year, Month, Day, Weekday, Hour, Minute, Second]

while 1:
    ut = ds.UnixTime(*ds.DateTime())
    print(ut)
    now_ut = ds.UnixTime(*ds.DateTime())
    while now_ut < ut + 1:
        now_ut = ds.UnixTime(*ds.DateTime())
        time.sleep(0.01)