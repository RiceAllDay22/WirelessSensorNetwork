# Default template for Digi projects
import XBee
import time
import xbee
transmit = 1


try:
    TARGET_NODE_ID = 'CentralBoard'
    device = XBee.find_device(TARGET_NODE_ID)
    addr64 = device['sender_eui64']
    rec_online = 1
except:
    rec_online = 0


bn = 3
while 1:
    if rec_online == 1 and transmit == 1:
        #XBee.transmit(addr64, bytes([3, 10, 20, 30, 40, 50, 60, 70, 80, 90]))
        received_msg = xbee.receive()
        if received_msg:
            sender = received_msg['sender_eui64']
            payload = received_msg['payload']
            print(int(payload))

    time.sleep(3)