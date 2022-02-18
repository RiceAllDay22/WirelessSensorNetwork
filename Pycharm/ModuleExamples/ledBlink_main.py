import machine
import time

dio2 = machine.Pin("D2", machine.Pin.OUT, value = 0)

while 1:
    dio2.value(1)
    time.sleep(1)
    dio2.value(0)
    time.sleep(1)