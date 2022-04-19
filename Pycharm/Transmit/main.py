# Default template for Digi projects

import time
import xbee
import network
from machine import ADC

bn = network.get_node_id()
print(bn)
addr64, rec_online = network.connect()

while 1:
    battery_pin = ADC("D0")
    vcc = battery_pin.read()
    bv1 = vcc // 256
    bv2 = vcc - bv1 * 256
    xbee.transmit(addr64, bytes([bv1, bv2]))
    time.sleep(1)