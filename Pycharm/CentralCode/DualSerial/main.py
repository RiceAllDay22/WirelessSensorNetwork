import micropython

import sys
import time
import machine

userButton = machine.Pin("D4", machine.Pin.IN)
micropython.kbd_intr(-1)


while 1:
    a = sys.stdin.buffer.read()
    #a = sys.stdout.buffer.read(1)
    if a != None:
        len_a = len(a)
        b_array = []
        for i in range(len_a):
            b_array.append(a[i])
        print('xbee got:', a, b_array)


        #for i in range(len_a):
            #print('xbee got:', a[i], len(a[i]), int.from_bytes(a[i], 'big'))
    else:
        print('xbee got:', a)
    #print('xbee got:', a)
    time.sleep(1)

    if userButton.value() == 0:
        print('Button')
        exit()


