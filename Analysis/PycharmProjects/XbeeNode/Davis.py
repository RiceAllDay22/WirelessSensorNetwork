from machine import ADC, Pin
import time

wd_pin = ADC("D0")
bit1 = Pin("D2", Pin.IN)
bit2 = Pin("D3", Pin.IN)
bit3 = Pin("D4", Pin.IN)
bit4 = Pin("D5", Pin.IN)
MR_pin = Pin("D19", Pin.OUT)

def BoolArrayToByte(boolArray):
	result = 0
	for i in range(0,4):
		if (boolArray[i]):
			result = result | (1 << i)
	return result

def MR():
	MR_pin.value(1)
	time.sleep(0.001)
	MR_pin.value(0)

def ws():
	ws_value_binary = [bit1.value(), bit2.value(), bit3.value(), bit4.value()]
	ws_value_decimal = BoolArrayToByte(ws_value_binary)
	MR()
	return ws_value_decimal


def wd():
	x = wd_pin.read()
	wd_value = (x-0)*(360-1) / (4095-0) + 0
	return int(wd_value)