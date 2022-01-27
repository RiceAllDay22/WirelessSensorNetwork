#Last Updated on 1-18-2022
import sys
import time
import xbee
import machine
import micropython

userButton = machine.Pin("D4", machine.Pin.IN)
micropython.kbd_intr(-1)

while 1:
    #Check for incoming data via XBee
    received_msg = xbee.receive()
    if received_msg:
        sender = received_msg['sender_eui64']
        payload = received_msg['payload']

        for i in range(0, len(payload)):
            if i == len(payload)-1:
                print(payload[i])
            else:
                print(payload[i], end=",")

    #Check for incoming data via Serial
    ser_msg = sys.stdin.buffer.read()
    if ser_msg:
        len_msg = len(ser_msg)
        b_array = []
        for b in range(len_msg):
            b_array.append(ser_msg[b])
        print('xbee got:', ser_msg, b_array)

        #If Time Sync, then broadcast to entire network
        try:
            xbee.transmit(xbee.ADDR_BROADCAST, bytes(ser_msg))
        except Exception as e:
            print("Transmit failure: %s" % str(e))
    #else:
    #    print('xbee has:', ser_msg)

    #Check for User Button press
    if userButton.value() == 0:
        print('STOP CODE')
        sys.exit()

    #Wait
    time.sleep(1)