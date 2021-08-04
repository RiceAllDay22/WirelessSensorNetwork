# Default template for Digi projects

from machine import Pin, ADC
import time

wd_pin = ADC("D0")
bit1   = Pin("D2", Pin.IN)
bit2   = Pin("D3", Pin.IN)
bit3   = Pin("D4", Pin.IN)
bit4   = Pin("D5", Pin.IN)
MR_pin = Pin("D19", Pin.OUT)

#bit_array = array([bit1.value, bit2.value(), bit3.value()], dtype= bool )


def wd():
	x  = wd_pin.read()
	wd = (x-0)*(360-1) / (4095-0) + 0
	print(x, wd)

def ws():
	bit_array = np.array([bit1.value, bit2.value(), bit3.value()], dtype=bool)
	print(bit_array)
	#print(bit1.value(), bit2.value(), bit3.value(), bit4.value())

def MR():
	MR_pin.value(1)
	MR_pin.value(0)

while True:
    ws()
    wd()
    time.sleep(1)