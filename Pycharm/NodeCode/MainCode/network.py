import xbee

# Function: Convert ppm from 16-bit integer to 2 bytes
def ppm_to_byte(ppm):
    b1 = ppm // 256
    b2 = ppm - b1 * 256
    return b1, b2


# Function: Convert ppm from 2 bytes to 16-bit integer
def byte_to_ppm(b1, b2):
    ppm = b1 * 256 + b2
    return ppm


# Function: Convert unixtime from 32-bit integer to 4 bytes
def ut_to_byte(ut):
    b1 = ut // 256 ** 3
    b2 = ut // 256 ** 2 - b1 * 256
    b3 = ut // 256 ** 1 - b1 * 256 ** 2 - b2 * 256
    b4 = ut - b1 * 256 ** 3 - b2 * 256 ** 2 - b3 * 256
    return b1, b2, b3, b4


# Function: Convert unixtime from 4 bytes to 32-bit integer
def byte_to_ut(b1, b2, b3, b4):
    ut = b1 * 256 ** 3 + b2 * 256 ** 2 + b3 * 256 + b4
    return ut


#Function: Convert wind direction and temperature from separate integers to 2 bytes
def windtemp_to_byte(wd, temp):
    temp += 40
    b1 = wd // 2
    if (wd%2) == 1:
        b2 = temp + 128 # wind dir is an odd number
    else:
        b2 = temp # wind dir is an even number
    return b1, b2


#Function: Convert wind direction and temperature from 2 bytes to separate integers
def byte_to_windtemp(b1, b2):
    if b2 > 127:
        wd = b1*2 + 1
        temp = b2 - 40 - 128
    else:
        wd = b1*2
        temp = b2 - 40
    return wd, temp


def find_device(node_id):
    for dev in xbee.discover():
        if dev['node_id'] == node_id:
            return dev
    return None


def connect():
    try:
        TARGET_NODE_ID = 'CentralBoard'
        device = find_device(TARGET_NODE_ID)
        addr64 = device['sender_eui64']
        rec_online = 1
    except:
        addr64 = None
        rec_online = 0
    return [addr64, rec_online]


def get_node_id():
    NODE_ID = xbee.atcmd("NI")
    if NODE_ID == 'Node#1':
        bn = 1
    elif NODE_ID == 'Node#2':
        bn = 2
    elif NODE_ID == 'Node#3':
        bn = 3
    else:
        bn = 111
    return bn
