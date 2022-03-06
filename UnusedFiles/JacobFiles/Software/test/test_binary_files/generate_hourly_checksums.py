"""Generate Hourly Checksums.

This file calculates the expected checksums for the first 24 hourly files of a given node, given a
start time, and a constant CO2 sensor value.

This file is a part of the Wireless Sensor Network project.
(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
"""

import numpy as np
import time
import datetime
import binascii
from datetime import timezone

CONSTANT_VALUE = 0xA1D5762F
DT = datetime.datetime(2020, 1, 1, 0, 0, 0)
SIZE = 3600
UNIXTIME = DT.replace(tzinfo=timezone.utc).timestamp()




for j in range(24):
    array = np.arange(SIZE*2, dtype="<u4").reshape(-1,2)
    array[:, 1] = CONSTANT_VALUE
    array[:, 0] = [UNIXTIME+i+1+(j*SIZE) for i in range(SIZE)]

    b = array.tobytes()
    
    crc = 0
    for i in range(SIZE):
        byt = b[(i*8):(i*8)+8]
        crc = binascii.crc32(byt, crc)
        
    print(j+1, ":", hex(crc).upper())