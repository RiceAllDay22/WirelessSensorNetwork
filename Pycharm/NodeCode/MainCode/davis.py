from machine import ADC, Pin
import time
import xbee

wd_pin = ADC("D2")  # ANEM_DIR in schematic
bit1 = Pin("D4", Pin.IN)  # COUNT_0 in schematic
bit2 = Pin("D5", Pin.IN)  # COUNT_1 in schematic
bit3 = Pin("D7", Pin.IN)  # COUNT_2 in schematic
bit4 = Pin("D9", Pin.IN)  # COUNT_3 in schematic
bit5 = Pin("D12", Pin.IN)  # COUNT_4 in schematic
bit6 = Pin("D17", Pin.ALT)  # COUNT_5 in schematic
bit7 = Pin("D18", Pin.ALT)  # COUNT_6 in schematic
bit8 = Pin("D16", Pin.ALT)  # COUNT_7 in schematic
MR_pin = Pin("D15", Pin.OUT)  # COUNT_RST in schematic
MR_pin.value(0)


# Function to convert an array of booleans to an integer
def BoolToByte(boolArray):
    result = 0
    for i in range(0, 8):
        if boolArray[i]:
            result = result | (1 << i)
    return result


# Function to reset the counter chip. Makes all the bits go to zero.
def MR():
    MR_pin.value(1)
    time.sleep(0.1)
    MR_pin.value(0)


# Function to read integer value given by the counter-chip
def ws():
    ws_binary = [bit1.value(), bit2.value(), bit3.value(), bit4.value(), bit5.value(), bit6.value(), bit7.value(),
                 bit8.value()]
    ws_integer = BoolToByte(ws_binary)
    MR()
    return ws_integer


# Function to read the analog reading of the anemometer
def wd(dir_offset):
    x = wd_pin.read()  # Reads analog value. Range is 0 to 4095.
    raw_dir = (x - 0) * (360 - 1) / (4095 - 0) + 1  # Converts analog to direction. Range is 1 to 360.
    new_dir = int(raw_dir) + int(dir_offset)  # Adds directional offset of the wind vane.

    if new_dir > 360:  # If new_dir is above the range of 1 to 360, then readjust it.
        new_dir = new_dir - 360
    elif new_dir < 1:  # If new_dir is below the range of 1 to 360, then readjust it.
        new_dir = new_dir + 360

    return new_dir
