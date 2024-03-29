# Last Updated 1-18-2022

import time
import xbee
import rtc
from machine import Pin, ADC, I2C

transmit_active = 1
bn = 1


i2c = I2C(1, freq=32000)  # DS3231 is 32kHz, SCD-30 is 50kHz, # ORIGINAL: 40kHz
ds = rtc.DS3231(i2c)


def find_device(node_id):
    for dev in xbee.discover():
        if dev['node_id'] == node_id:
            return dev
    return None


def transmit(address, message):
    try:
        xbee.transmit(address, message)
        # print("Data sent successfully")
    except Exception as e:
        print("Transmit failure: %s" % str(e))


print("Hello World!")

# Connect to CentralHub
try:
    TARGET_NODE_ID = 'CentralBoard'
    device = find_device(TARGET_NODE_ID)
    addr64 = device['sender_eui64']
    rec_online = 1
except:
    rec_online = 0

print("Rec_online:", rec_online)
print("Tramsmit:", transmit_active)

while 1:
    ut = ds.UnixTime(*ds.DateTime())
    print(ut)
    # If connection to CentralHub is active and if TransmitMode is on, then
    if rec_online == 1 and transmit_active == 1:
        # Send Fake Data
        transmit(addr64, bytes([bn, 10, 20, 30, 40, 50, 60, 70, 80, 90]))

        # Check if there is an incoming broadcast
        received_msg = xbee.receive()
        if received_msg:
            print("Incoming broadcast from Central Hub:")
            sender = received_msg['sender_eui64']
            payload = received_msg['payload']
            b = payload

            # Check if incoming data is a Time Sync from CentralHub
            if len(b) == 8:
                print("Time Sync to %s-%s-%s %s:%s:%s" % (
                    payload[1] + 2000, payload[2], payload[3], payload[4], payload[5], payload[6]))
                ds.DateTime([payload[1] + 2000, payload[2], payload[3], payload[4], payload[5], payload[6]])

    else:
        print("Did not send")

    # Wait
    time.sleep(3)
