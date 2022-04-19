from machine import I2C
import sensirion
import time

i2c = I2C(1, freq=32000)  # DS3231 is 32kHz, SCD-30 is 50kHz
scd = sensirion.SCD30(i2c, 0x61)
scd.set_measurement_interval(2)
scd.set_altitude_comp(1300)
scd.start_continous_measurement()

while 1:
    conc, temp, humid = scd.getData()
    print(conc, temp, humid)
    time.sleep(3)
