import machine
import DS3231
import time

i2c = machine.I2C(1, freq=32000)  # DS3231 is 32kHz, SCD-30 is 50kHz, # ORIGINAL: 40kHz
ds = DS3231.DS3231(i2c)
#ds.DateTime([2022, 4, 14, 16, 40, 0]) # [Year, Month, Day, Hour, Minute, Second]

while 1:
    ut = ds.UnixTime(*ds.DateTime())
    print(ut)
    now_ut = ds.UnixTime(*ds.DateTime())
    while now_ut < ut + 1:
        now_ut = ds.UnixTime(*ds.DateTime())
        time.sleep(0.01)