import xbee

# Function: 16 bit to 2 bytes
def ppm_to_byte(ppm):
    b1 = ppm // 256
    b2 = ppm - b1 * 256
    return b1, b2


# Function: 2 bytes to 16 bit
def byte_to_ppm(b1, b2):
    ppm = b1 * 256 + b2
    return ppm


# Function: 8 bit to 1 byte
def temp_to_byte(temp):
    b1 = temp + 40
    return b1


# Function: 1 byte to 8 bit
def byte_to_temp(b1):
    temp = b1 - 40
    return temp


# Function: 32 bit to 4 bytes
def ut_to_byte(ut):
    b1 = ut // 256 ** 3
    b2 = ut // 256 ** 2 - b1 * 256
    b3 = ut // 256 ** 1 - b1 * 256 ** 2 - b2 * 256
    b4 = ut - b1 * 256 ** 3 - b2 * 256 ** 2 - b3 * 256
    return b1, b2, b3, b4


# Function: 4 bytes to 32 bit
def byte_to_ut(b1, b2, b3, b4):
    ut = b1 * 256 ** 3 + b2 * 256 ** 2 + b3 * 256 + b4
    return ut


# Function: ws and wd to 2 bytes
def wind_to_byte(ws, wd):
    b1 = wd // 2

    if (wd % 2) == 1:
        b2 = ws + 128  # wd is odd
    else:
        b2 = ws  # wd is even
    return b1, b2


# Function: 2 bytes to ws and wd
def byte_to_wind(b1, b2):
    if b2 > 127:
        wd = b1 * 2 + 1
        ws = b2 - 128
    else:
        wd = b1 * 2
        ws = b2
    return ws, wd


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
    if NODE_ID == 'PCBBoardNew':
        bn = 1
    elif NODE_ID == 'RyanBoard':
        bn = 2
    else:
        bn = 111
    return bn
