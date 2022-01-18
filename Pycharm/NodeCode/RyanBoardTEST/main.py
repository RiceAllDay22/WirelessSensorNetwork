# Default template for Digi projects
import time
import xbee
import XBee
import machine
import DS3231

transmit = 1

i2c = machine.I2C(1, freq=32000)  # DS3231 is 32kHz, SCD-30 is 50kHz, # ORIGINAL: 40kHz
ds = DS3231.DS3231(i2c)
# ds.DateTime([2022, 1, 10, 11, 0, 0])
# year, month, day, hour, minute, sec

try:
    TARGET_NODE_ID = 'CentralBoard'
    device = XBee.find_device(TARGET_NODE_ID)
    addr64 = device['sender_eui64']
    rec_online = 1
except:
    rec_online = 0

print('rec_online:', rec_online)
bn = 3
while 1:
    if rec_online == 1 and transmit == 1:
        XBee.transmit(addr64, bytes([3, 10, 20, 30, 40, 50, 60, 70, 80, 90]))
        received_msg = xbee.receive()
        if received_msg:
            sender = received_msg['sender_eui64']
            payload = received_msg['payload']
            b = payload

            if len(b) == 6:
                print('Sync')
                y = 2000 + b[0]
                m = b[1]
                d = b[2]
                hh = b[3]
                mm = b[4]
                ss = b[5]

                ds.DateTime([y, m, d, hh, mm, ss])
                print(payload)

    print(ds.UnixTime(*ds.DateTime()))
    time.sleep(3)
