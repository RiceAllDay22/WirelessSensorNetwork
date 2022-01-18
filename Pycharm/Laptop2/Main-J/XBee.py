# Source: Digi
import xbee


def find_device(node_id):
    for dev in xbee.discover():
        if dev['node_id'] == node_id:
            return dev
    return None


def transmit(address, message):
    try:
        xbee.transmit(address, message)
        #print("Data sent successfully")
    except Exception as e:
        print("Transmit failure: %s" % str(e))
