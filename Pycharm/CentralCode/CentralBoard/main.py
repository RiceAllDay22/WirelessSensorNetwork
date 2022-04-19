'''
    Last updated: 4-19-2022
    Adriann Liceralde
    Wireless Sensor Network Project

    This code operates the XBee that is dedicated to be the Central Hub.
    This XBee continuously checks for data received from other nodes within the network.
    In addition, the XBee will transmit a time synchronization to all the nodes.
'''

# IMPORT LIBRARIES
import sys
import time
import xbee
from machine import Pin
import micropython  # For some reason, PyCharm thinks micropython is not a Library, but it is.

# SETUP PINS
stopButton = Pin("D4", mode=Pin.IN, pull=Pin.PULL_UP)  # This is the User button on the Grove board.
syncButton = Pin("D0", mode=Pin.IN, pull=Pin.PULL_UP)  # This is the Commissioning button on the Grove board.
micropython.kbd_intr(-1)  # This disables the keyboard interrupt feature
print("CentralBoard online")

# MAIN LOOP
while 1:
    # Check for incoming data via XBee
    received_msg = xbee.receive()
    if received_msg:
        sender = received_msg['sender_eui64']
        payload = received_msg['payload']

        # Print the incoming data to the Serial line
        for i in range(0, len(payload)):
            if i == len(payload) - 1:
                print(payload[i])
            else:
                print(payload[i], end=",")

    # Check for incoming data from the Computer via the Serial line
    ser_msg = sys.stdin.buffer.read()
    if ser_msg:
        len_msg = len(ser_msg)
        b_array = []
        for b in range(len_msg):
            b_array.append(ser_msg[b])

        # If the incoming data is for the Time Sync, then broadcast the unix timestamp to entire network
        if len(b_array) == 8 and b_array[0] == 255 and b_array[-1] == 255:
            try:
                xbee.transmit(xbee.ADDR_BROADCAST, ser_msg)
                print("Transmit success")
            except Exception as e:
                print("Transmit failure: %s" % str(e))

    # Check for User Button press -> Stop execution of the code
    if stopButton.value() == 0:
        print('STOP CODE')
        sys.exit()

    # Check for Test Button press -> Send signal along Serial line to request a unix timestamp
    if syncButton.value() == 0:
        print([256, 1, 256])

    # Wait
    time.sleep(1)
