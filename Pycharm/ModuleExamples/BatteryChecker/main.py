# Default template for Digi projects
from machine import Pin, ADC
import time

vd = ADC("D0")

def func(vs, vr):
    for i in range(1000):
        adc = vd.read()
        v = adc/4095 * vs
        vcc = v * vr
        print(adc, v, vcc, vcc/vs)
        time.sleep(0.2)
