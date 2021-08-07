from machine import I2C
import DS3231
import SCD30
import time
from Davis import wd, ws, MR

SECONDS_FROM_1970_TO_2000 = 946684800
daysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30]


def time2ulong(days, hh, mm, ss):
    return ((days * 24 + hh) * 60 + mm) * 60 + ss

def date2days(y, m, d):
    y -= 2000
    days = d
    for i in range(m-1):
        days += daysInMonth[i]
    if ((m > 2) and (y % 4 == 0) ):
        days += 1
    return days + 365 * y + (y + 3) // 4 - 1

def unixtime(y, m, d, hh, mm, ss):
    t = 0
    days = date2days(y, m, d)
    t = time2ulong(days, hh, mm, ss)
    t += SECONDS_FROM_1970_TO_2000
    return t


i2c = I2C(1)
scd = SCD30.SCD30(i2c, 0x61)
ds = DS3231.DS3231(i2c)
ds.DateTime([2021, 8, 7, 1, 16, 30, 0])
datetime = [2070, 8, 7, 16, 30, 0]
unix = unixtime(*datetime)
print(unix)
print('checkcheck')


MR()








while 1:
    windDir = wd()
    dt = ds.DateTime()


    co2 = None

    while 1:
        try:
            co2 = scd.read_measurement()
            if co2[0] == co2[0]:
                break
        except:
            print("Error Trying again...")

    print(dt, co2, windDir, ws())
    time.sleep(3)

