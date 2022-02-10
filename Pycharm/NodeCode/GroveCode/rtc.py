# Source: https://github.com/micropython-Chinese-Community/mpy-lib/tree/master/misc/DS3231

'''
    DS3231 RTC drive

    Author: shaoziyang
    Date:   2018.3

    https://github.com/micropython-Chinese-Community/mpy-lib/tree/master/misc/DS3231

    Edited by Adriann Liceralde
    2/9/2022
'''
from machine import I2C, Pin
import time

DS3231_I2C_ADDR = (0x68)
DS3231_REG_SEC = (0x00)
DS3231_REG_MIN = (0x01)
DS3231_REG_HOUR = (0x02)
DS3231_REG_WEEKDAY = (0x03)
DS3231_REG_DAY = (0x04)
DS3231_REG_MONTH = (0x05)
DS3231_REG_YEAR = (0x06)
DS3231_REG_A1SEC = (0x07)
DS3231_REG_A1MIN = (0x08)
DS3231_REG_A1HOUR = (0x09)
DS3231_REG_A1DAY = (0x0A)
DS3231_REG_A2MIN = (0x0B)
DS3231_REG_A2HOUR = (0x0C)
DS3231_REG_A2DAY = (0x0D)
DS3231_REG_CTRL = (0x0E)
DS3231_REG_STA = (0x0F)
DS3231_REG_AGOFF = (0x10)
DS3231_REG_TEMP = (0x11)

PER_DISABLE = (0)
PER_MINUTE = (1)
PER_HOUR = (2)
PER_DAY = (3)
PER_WEEKDAY = (4)
PER_MONTH = (5)

SECONDS_FROM_1970_TO_2000 = 946684800
daysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30]


class DS3231():
    def __init__(self, i2c):
        success = 0
        while success == 0:
            devices = i2c.scan()  # Line not in original
            if DS3231_I2C_ADDR in devices:
                success = 1
            else:
                print("Did not find slave %d in scan: %s" % (DS3231_I2C_ADDR, devices))
                time.sleep(1)
        self.i2c = i2c
        self.setReg(DS3231_REG_CTRL, 0x4C)

    def DecToHex(self, dat):
        return (dat // 10) * 16 + (dat % 10)

    def HexToDec(self, dat):
        return (dat // 16) * 10 + (dat % 16)

    def setReg(self, reg, dat):
        self.i2c.writeto(DS3231_I2C_ADDR, bytearray([reg, dat]))

    # def getReg(self, reg):
    #     self.i2c.writeto(DS3231_I2C_ADDR, bytearray([reg]))
    #     return self.i2c.readfrom(DS3231_I2C_ADDR, 1)[0]

    # def getReg(self, reg):
    #     try:
    #         self.i2c.writeto(DS3231_I2C_ADDR, bytearray([reg]))
    #     except:
    #         print("error here")
    #     try:
    #         a = self.i2c.readfrom(DS3231_I2C_ADDR, 1)[0]
    #     except:
    #         print("Error there")
    #     return a

    def getReg(self, reg):
        while 1:
            try:
                self.i2c.writeto(DS3231_I2C_ADDR, bytearray([reg]))
                read = self.i2c.readfrom(DS3231_I2C_ADDR, 1)[0]
                if read != None:
                    break
            except:
                print('------------------------------------------------------------------------------')
                print("________________getReg Error__________---------------------------------------_______")
                print('------------------------------------------------------------------------------')
        return read

    def Second(self, second=None):
        if second == None:
            return self.HexToDec(self.getReg(DS3231_REG_SEC))
        else:
            self.setReg(DS3231_REG_SEC, self.DecToHex(second % 60))

    def Minute(self, minute=None):
        if minute == None:
            return self.HexToDec(self.getReg(DS3231_REG_MIN))
        else:
            self.setReg(DS3231_REG_MIN, self.DecToHex(minute % 60))

    def Hour(self, hour=None):
        if hour == None:
            return self.HexToDec(self.getReg(DS3231_REG_HOUR))
        else:
            self.setReg(DS3231_REG_HOUR, self.DecToHex(hour % 24))

    def Weekday(self, weekday=None):
        if weekday == None:
            return self.HexToDec(self.getReg(DS3231_REG_WEEKDAY))
        else:
            self.setReg(DS3231_REG_WEEKDAY, self.DecToHex(weekday % 8))

    def Day(self, day=None):
        if day == None:
            return self.HexToDec(self.getReg(DS3231_REG_DAY))
        else:
            self.setReg(DS3231_REG_DAY, self.DecToHex(day % 32))

    def Month(self, month=None):
        if month == None:
            return self.HexToDec(self.getReg(DS3231_REG_MONTH))
        else:
            self.setReg(DS3231_REG_MONTH, self.DecToHex(month % 13))

    def Year(self, year=None):
        if year == None:
            return self.HexToDec(self.getReg(DS3231_REG_YEAR)) + 2000
        else:
            self.setReg(DS3231_REG_YEAR, self.DecToHex(year % 100))

    def Date(self, dat=None):
        if dat == None:
            return [self.Year(), self.Month(), self.Day()]
        else:
            self.Year(dat[0] % 100)
            self.Month(dat[1] % 13)
            self.Day(dat[2] % 32)

    def Time(self, dat=None):
        if dat == None:
            return [self.Hour(), self.Minute(), self.Second()]
        else:
            self.Hour(dat[0] % 24)
            self.Minute(dat[1] % 60)
            self.Second(dat[2] % 60)

    # def DateTime(self, dat = None):
    #     if dat == None:
    #         return self.Date() + [self.Weekday()] + self.Time()
    #     else:
    #         self.Year(dat[0])
    #         self.Month(dat[1])
    #         self.Day(dat[2])
    #         self.Weekday(dat[3])
    #         self.Hour(dat[4])
    #         self.Minute(dat[5])
    #         self.Second(dat[6])

    def DateTime(self, dat=None):
        if dat == None:
            return self.Date() + self.Time()
        else:
            self.Year(dat[0])
            self.Month(dat[1])
            self.Day(dat[2])
            self.Hour(dat[3])
            self.Minute(dat[4])
            self.Second(dat[5])

    def ALARM(self, day, hour, minute, repeat):
        IE = self.getReg(DS3231_REG_CTRL)
        if repeat == PER_DISABLE:
            self.setReg(DS3231_REG_CTRL, IE & 0xFC)  # disable ALARM OUT
            return
        IE |= 0x46
        self.setReg(DS3231_REG_CTRL, IE)
        M2 = M3 = M4 = 0x80
        DT = 0
        if repeat == PER_MINUTE:
            pass
        elif repeat == PER_HOUR:
            M2 = 0
        elif repeat == PER_DAY:
            M2 = M3 = 0
        else:
            M2 = M3 = M4 = 0
            if repeat == PER_WEEKDAY:
                DT = 0x40
        self.setReg(DS3231_REG_A2MIN, self.DecToHex(minute % 60) | M2)
        self.setReg(DS3231_REG_A2HOUR, self.DecToHex(hour % 24) | M3)
        self.setReg(DS3231_REG_A2DAY, self.DecToHex(day % 32) | M4 | DT)

    def ClearALARM(self):
        self.setReg(DS3231_REG_STA, 0)

    def Temperature(self):
        t1 = self.getReg(DS3231_REG_TEMP)
        t2 = self.getReg(DS3231_REG_TEMP + 1)
        if t1 > 0x7F:
            return t1 - t2 / 256 - 256
        else:
            return t1 + t2 / 256

    # def time2ulong(self, days, hh, mm, ss):
    #     return ((days * 24 + hh) * 60 + mm) * 60 + ss

    def time2ulong(self, days, hh, mm, ss):
        try:
            a = ((days * 24 + hh) * 60 + mm) * 60 + ss
        except:
            print('------------------------------')
            print(type(days), type(hh), type(mm), type(ss))
        return a


    def date2days(self, y, m, d):
        y -= 2000
        days = d
        for i in range(m - 1):
            days += daysInMonth[i]
        if ((m > 2) and (y % 4 == 0)):
            days += 1
        return days + 365 * y + (y + 3) // 4 - 1

    # def UnixTime(self, y, m, d, Weekday, hh, mm, ss):
    def UnixTime(self, y, m, d, hh, mm, ss):
        days = self.date2days(y, m, d)
        ut = self.time2ulong(days, hh, mm, ss)
        ut += SECONDS_FROM_1970_TO_2000
        return ut

    def get_unixtime(self):
        while 1:
            try:
                dt = self.DateTime()
                if dt[0] == dt[0]:
                    break
            except:
                print("RTC Error Trying again...")
        ut = self.UnixTime(*dt)
        return ut
