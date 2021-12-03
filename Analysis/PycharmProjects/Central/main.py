import xbee
import machine
import time
import datetime
MESSAGE = 1638513297
dio = machine.Pin("P2", machine.Pin.IN)

#datetime.datetime.now()

while True:
    received_msg = xbee.receive()
    if received_msg:
        sender = received_msg['sender_eui64']
        payload = received_msg['payload']

        for i in range(0, len(payload)):
            if i == len(payload)-1:
                print(payload[i])
            else:
                print(payload[i], end = ",")

    if dio.value() == 1:
        try:
            xbee.transmit(xbee.ADDR_BROADCAST, str(MESSAGE))
            print("Data sent successfully")
            time.sleep(1)
        except Exception as e:
            print("Transmit failure: %s" % str(e))