from machine import ADC, Pin
import time

wd_pin = ADC("D2")
bit1 = Pin("D4", Pin.IN)
bit2 = Pin("D5", Pin.IN)
bit3 = Pin("D7", Pin.IN)
bit4 = Pin("D9", Pin.IN)
bit5 = Pin("D12", Pin.IN)
bit6 = Pin("D17")
bit7 = Pin("D18")
bit8 = Pin("D16")
MR_pin = Pin("D15")

def BoolToByte(boolArray):
    result = 0
    for i in range(0, 8):
        if boolArray[i]:
            result = result | (1 << i)
    return result

def MR():
    MR_pin.value(1)
    time.sleep(0.1)
    MR_pin.value(0)

def ws():
    ws_binary = [bit1.value(), bit2.value(), bit3.value(), bit4.value(), bit5.value(), bit6.value(), bit7.value(), bit8.value()]
    ws_integer = BoolToByte(ws_binary)
    MR()
    return ws_integer


def wd():
    x = wd_pin.read()
    wd_value = (x - 0) * (360 - 1) / (4095 - 0) + 0
    return int(wd_value)
