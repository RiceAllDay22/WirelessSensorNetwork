import xbee
import XBee
import machine
import time
from sys import stdout, stdin
#import datetime
MESSAGE = 1638513297
dio = machine.Pin("P2", machine.Pin.IN)

#datetime.datetime.now()



try:
    TARGET_NODE_ID = 'BlueGrove'
    device = XBee.find_device(TARGET_NODE_ID)
    addr64 = device['sender_eui64']
    rec_online = 1
except:
    rec_online = 0
print(rec_online)


while True:
    #print(stdin.buffer.read(), 1)
    #print(stdin.read(), 1)
    #print(stdin.read(0), 1)
    #print(stdin.buffer.read(0), 1)

    #print(stdin.buffer.read(1), 1)
    received_msg = xbee.receive()
    if received_msg:
        sender = received_msg['sender_eui64']
        payload = received_msg['payload']

        for i in range(0, len(payload)):
            if i == len(payload)-1:
                print(payload[i])
            else:
                print(payload[i], end = ",")



        #stdin.buffer.write(bytes(22))
        #stdout.buffer.write(bytes(22))


        print('1')
        XBee.transmit(addr64, str(stdin.buffer.read() ) )
        print('2')
        XBee.transmit(addr64, str(stdout.buffer.read() ))
        print('3')
        XBee.transmit(addr64, str(stdin.buffer.readline() ) )
        print('4')
        XBee.transmit(addr64, str(stdout.buffer.readline() ))

        #-XBee.transmit(addr64, str(stdin.read()))
        #-XBee.transmit(addr64, str(stdin.read(0)))
        #XBee.transmit(addr64, str(stdin.buffer.read()))
        #XBee.transmit(addr64, str(stdin.buffer.read(0)))
        #XBee.transmit(addr64, str(stdin.read(1)))
        #XBee.transmit(addr64, str(stdin.readline()))##
        #XBee.transmit(addr64, str(stdin.readline(0)))
        ##imXBee.transmit(addr64, str(stdin.readlines(0)))



#    if dio.value() == 2:
#        try:
#            xbee.transmit(xbee.ADDR_BROADCAST, str(MESSAGE))
#            print("Data sent successfully")
#            time.sleep(1)
#        except Exception as e:
#            print("Transmit failure: %s" % str(e))