# 10/19/2021 DAVIS

# IMPORT LIBRARIES
import machine
import time
import Davis
import gc

# MISCELLANEOUS SETUPS
BUTTON_Pin = machine.Pin("D3", machine.Pin.IN)
dir_offset = 0  # Specify the angular offset of the actual wind vane from true North.
Davis.MR()  # Reset Counter Chip
gc.collect()

while 1:
    windDir = Davis.wd(dir_offset)
    windCyc = Davis.ws()

    print(windDir, windCyc)
    time.sleep(3)