# https://github.com/peterhinch/micropython_eeprom
# bdevice.py Hardware-agnostic base classes.
# BlockDevice Base class for general block devices e.g. EEPROM, FRAM.
# FlashDevice Base class for generic Flash memory (subclass of BlockDevice).
# Documentation in BASE_CLASSES.md

# Released under the MIT License (MIT). See LICENSE.
# Copyright (c) 2019 Peter Hinch

from micropython import const
import uos
import time


class BlockDevice:

    def __init__(self, nbits, nchips, chip_size):
        self._c_bytes = chip_size  # Size of chip in bytes
        self._a_bytes = chip_size * nchips  # Size of array
        self._nbits = nbits  # Block size in bits
        self._block_size = 2**nbits
        self._rwbuf = bytearray(1)

    def __len__(self):
        return self._a_bytes

    def __setitem__(self, addr, value):
        if isinstance(addr, slice):
            return self._wslice(addr, value)
        self._rwbuf[0] = value
        self.readwrite(addr, self._rwbuf, False)

    def __getitem__(self, addr):
        if isinstance(addr, slice):
            return self._rslice(addr)
        return self.readwrite(addr, self._rwbuf, True)[0]

    # Handle special cases of a slice. Always return a pair of positive indices.
    def _do_slice(self, addr):
        addr = str(addr)[6:-7]
        start, stop = addr.split(", ")
        return int(start), int(stop)

    def _wslice(self, addr, value):
        start, stop = self._do_slice(addr)
        try:
            if len(value) == (stop - start):
                res = self.readwrite(start, value, False)
            else:
                raise RuntimeError('Slice must have same length as data')
        except TypeError:
            raise RuntimeError('Can only assign bytes/bytearray to a slice')
        return res

    def _rslice(self, addr):
        start, stop = self._do_slice(addr)
        buf = bytearray(stop - start)
        return self.readwrite(start, buf, True)

    # IOCTL protocol.
    def sync(self):  # Nothing to do for unbuffered devices. Subclass overrides.
        return

    def readblocks(self, blocknum, buf, offset=0):
        self.readwrite(offset + (blocknum << self._nbits), buf, True)

    def writeblocks(self, blocknum, buf, offset=0):
        self.readwrite(offset + (blocknum << self._nbits), buf, False)

    # https://docs.micropython.org/en/latest/library/os.html#os.AbstractBlockDev.ioctl
    def ioctl(self, op, arg):  # ioctl calls: see extmod/vfs.h
        if op == 3:  # SYNCHRONISE
            self.sync()
            return
        if op == 4:  # BP_IOCTL_SEC_COUNT
            return self._a_bytes >> self._nbits
        if op == 5:  # BP_IOCTL_SEC_SIZE
            return self._block_size
        if op == 6:  # Ignore ERASE because handled by driver.
            return 0



# https://github.com/peterhinch/micropython_eeprom
# fram_i2c.py Driver for Adafruit 32K Ferroelectric RAM module (Fujitsu MB85RC256V)

# Released under the MIT License (MIT). See LICENSE.
# Copyright (c) 2019 Peter Hinch

_SIZE = const(32768)  # Chip size 32KiB
_ADDR = const(0x50)  # FRAM I2C address 0x50 to 0x57
_FRAM_SLAVE_ID = const(0xf8)  # FRAM device ID location
_MANF_ID = const(0x0a)
_PRODUCT_ID = const(0x510)


# A logical ferroelectric RAM made up of from 1 to 8 chips
class FRAM(BlockDevice):
    def __init__(self, i2c, verbose=True, block_size=9):
        self._i2c = i2c
        self._buf1 = bytearray(1)
        self._addrbuf = bytearray(2)  # Memory offset into current chip
        self._buf3 = bytearray(3)
        #self._nchips = self.scan(verbose, _SIZE)
        self._nchips = 1
        super().__init__(block_size, self._nchips, _SIZE)
        self._i2c_addr = 0x50  #None # i2c address of current chip

    def scan(self, verbose, chip_size):
        devices = self._i2c.scan()
        chips = [d for d in devices if d in range(_ADDR, _ADDR + 8)]
        nchips = len(chips)
        if nchips == 0:
            raise RuntimeError('FRAM not found.')
        if min(chips) != _ADDR or (max(chips) - _ADDR) >= nchips:
            raise RuntimeError('Non-contiguous chip addresses', chips)
        for chip in chips:
            if not self._available(chip):
                raise RuntimeError('FRAM at address 0x{:02x} reports an error'.format(chip))
        if verbose:
            s = '{} chips detected. Total FRAM size {}bytes.'
            print(s.format(nchips, chip_size * nchips))
        return nchips

    def _available(self, device_addr):
        res = self._buf3
        self._i2c.readfrom_mem_into(_FRAM_SLAVE_ID >> 1, device_addr << 1, res)
        manufacturerID = (res[0] << 4) + (res[1]  >> 4)
        productID = ((res[1] & 0x0F) << 8) + res[2]
        return manufacturerID == _MANF_ID and productID == _PRODUCT_ID

    # In the context of FRAM a page == a chip.
    # Args: an address and a no. of bytes. Set ._i2c_addr to correct chip.
    # Return the no. of bytes available to access on that chip.
    def _getaddr(self, addr, nbytes):  # Set up _addrbuf and i2c_addr
        if addr >= self._a_bytes:
            raise RuntimeError('FRAM Address is out of range')
        ca, la = divmod(addr, self._c_bytes)  # ca == chip no, la == offset into chip
        self._addrbuf[0] = (la >> 8) & 0xff
        self._addrbuf[1] = la & 0xff
        self._i2c_addr = _ADDR + ca
        return min(nbytes, self._c_bytes - la)

    def readwrite(self, addr, buf, read):
        nbytes = len(buf)
        mvb = memoryview(buf)
        start = 0  # Offset into buf.
        while nbytes > 0:
            npage = self._getaddr(addr, nbytes)  # No of bytes that fit on current chip
            if read:
                self._i2c.writeto(self._i2c_addr, self._addrbuf)
                self._i2c.readfrom_into(self._i2c_addr, mvb[start : start + npage])  # Sequential read
            else:
                self._i2c.writevto(self._i2c_addr, (self._addrbuf, buf[start: start + npage]))
            nbytes -= npage
            start += npage
            addr += npage
        return buf


# Return an FRAM array. Adapt for platforms other than Pyboard.
def get_fram(i2c):
    fram = FRAM(i2c)
    print('Instantiated FRAM')
    return fram


def test():
    fram = get_fram()
    sa = 1000
    for v in range(256):
        fram[sa + v] = v
    for v in range(256):
        if fram[sa + v] != v:
            print('Fail at address {} data {} should be {}'.format(sa + v, fram[sa + v], v))
            break
    else:
        print('Test of byte addressing passed')
    data = uos.urandom(30)
    sa = 2000
    fram[sa:sa + 30] = data
    if fram[sa:sa + 30] == data:
        print('Test of slice readback passed')


# ***** TEST OF HARDWARE *****
def full_test():
    fram = get_fram()
    page = 0
    for sa in range(0, len(fram), 256):
        data = uos.urandom(256)
        fram[sa:sa + 256] = data
        if fram[sa:sa + 256] == data:
            pass
            #print('Page {} passed'.format(page))
        else:
            print('Page {} readback failed.'.format(page))
        page += 1
    print('Complete')




def locator_reset(storage):
    storage[0:2] = b'\x00\x02'
    return None

def get_locator(storage):
    return storage[0:2]

def check(storage):
    for i in range(20):
        print(storage[i], end=" ")
    print("")
    return None

def retrieve_storage(locator_byt):
    locator_int = int.from_bytes(locator_byt, "big")
    print(locator_byt, locator_int)
    return None

def reset(storage):
    storage[0:20] = b'\x00' * 20
    time.sleep(1)
    locator_reset(storage)
    return None


def emergency_storage(storage, locator_byt, data, previous_ut, unix_included = False):
    
    # Get Data
    now_ut = int.from_bytes(data[1:5], "big")
    sensor_data = data[5:10]
    bs = now_ut - previous_ut
    data_to_store = sensor_data + bytes([bs])

    # Get FRAM Locator
    locator_int = int.from_bytes(locator_byt, "big")

    # Save Data to FRAM with Unix included
    if unix_included == True:
        storage[locator_int:locator_int + 10] = data[1:5] + data_to_store[0:6]
        time.sleep(1)
        locator_int = locator_int + 10

    # Save Data to FRAM without Unix included
    elif unix_included == False:
        print('Before:', storage[locator_int:locator_int + 6])
        storage[locator_int:locator_int + 6] = data_to_store
        time.sleep(1)
        print('After:', storage[locator_int:locator_int + 6])
        locator_int = locator_int + 6

    # Update FRAM Locator
    locator_byt = locator_int.to_bytes(2, "big")
    storage[0:2] = locator_byt
    print('Loc:', locator_byt[0] * 256 + locator_byt[1])

    previous_ut = now_ut

    return [locator_byt, previous_ut]


def unix_storage(storage, locator_byt, data):
    # Get FRAM Locator
    
    locator_int = int.from_bytes(locator_byt, "big")


