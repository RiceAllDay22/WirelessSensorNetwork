from machine import I2C
import DS3231
import SCD30
import time
from Davis import wd, ws, MR


i2c = I2C(1)
scd = SCD30.SCD30(i2c, 0x61)
ds = DS3231.DS3231(i2c)
ds.DateTime([2018,3,12,1,22,10,0])
MR()



while 1:
    scd.read_measurement()
    windDir = wd()
    dt = ds.DateTime()
    print(dt, scd.read_measurement(), windDir, ws())
    time.sleep(3)

