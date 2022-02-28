import sys
import numpy as np
import pyfirmata
import time
import adafruit_tca9548a

print("Checkpoint Libraries")

portName = 'COM4'
board = pyfirmata.Arduino(portName)


print(dir(board))
print(board.digital_ports())
print(board.digital())
print("Checkpoint I2C")

while True:
    board.digital[2].write(1)
    time.sleep(1)
    board.digital[2].write(0)
    time.sleep(1)