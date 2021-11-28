# Default template for Digi projects
import XBee
import time
transmit = 1


try:
    TARGET_NODE_ID = 'TH'
    device = XBee.find_device(TARGET_NODE_ID)
    addr64 = device['sender_eui64']
    rec_online = 1
except:
    rec_online = 0


bn = 3
while 1:
    if rec_online == 1 and transmit == 1:
        bs, bw1, bw2, bc1, bc2, bt = 200, 10, 20, 30, 40, 50
        XBee.transmit(addr64, bytes([bn, bs, bw1, bw2, bc1, bc2, bt, 255]))
    time.sleep(3)