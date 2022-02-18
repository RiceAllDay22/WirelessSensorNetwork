
import gc
print(gc.mem_free())
gc.collect()

import array
print(gc.mem_free())
gc.collect()

import xbee
print(gc.mem_free())
gc.collect()


TIME = array.array('I', [1630807372, 1630807375, 1630807378, 1630807381, 1630807384])
CONC = array.array('I', [510, 520, 530, 540, 550])
WCYC = array.array('I', [1, 2, 3, 4, 5])
WDIR = array.array('I', [10, 20, 30, 40, 50])

row1 = array.array('I', [1600000000, 500, 1, 10])
row2 = array.array('I', [1600000003, 505, 2, 20])
row3 = array.array('I', [1600000006, 510, 3, 30])

try:
    for i in range(0, len(TIME)):
        xbee.transmit(xbee.ADDR_BROADCAST, str(TIME[i]))
        xbee.transmit(xbee.ADDR_BROADCAST, str(CONC[i]))
        xbee.transmit(xbee.ADDR_BROADCAST, str(WCYC[i]))
        xbee.transmit(xbee.ADDR_BROADCAST, str(WDIR[i]))
    print("Data sent successfully")
except Exception as e:
    print("Transmit failure: %s" % str(e))
