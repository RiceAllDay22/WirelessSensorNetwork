'''
    Source: https://github.com/peterhinch/micropython_eeprom
    Released under the MIT License (MIT). See LICENSE.
    Copyright (c) 2019 Peter Hinch

    This code is a combination of two python files from the Source
    https://github.com/peterhinch/micropython_eeprom/blob/master/bdevice.py
    https://github.com/peterhinch/micropython_eeprom/blob/master/fram/fram_i2c.py


    Edited by Adriann Liceralde
    4/21/2022
'''

from micropython import const
import time
import fram
import xbee

_SIZE = const(32768)  # Chip size 32KiB
_ADDR = const(0x50)  # FRAM I2C address 0x50 to 0x57
_FRAM_SLAVE_ID = const(0xf8)  # FRAM device ID location
_MANF_ID = const(0x0a)
_PRODUCT_ID = const(0x510)


class BlockDevice:
    def __init__(self, nbits, nchips, chip_size):
        self._c_bytes = chip_size  # Size of chip in bytes
        self._a_bytes = chip_size * nchips  # Size of array
        self._nbits = nbits  # Block size in bits
        self._block_size = 2 ** nbits
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

    # def _wslice(self, addr, value):
    #     start, stop = self._do_slice(addr)
    #     try:
    #         if len(value) == (stop - start):
    #             res = self.readwrite(start, value, False)
    #         else:
    #             raise RuntimeError('Slice must have same length as data')
    #     except TypeError:
    #         raise RuntimeError('Can only assign bytes/bytearray to a slice') # NEED TO FIX THIS
    #     return res

    def _wslice(self, addr, value):
        start, stop = self._do_slice(addr)
        success = 0
        while success == 0:
            try:
                if len(value) == (stop - start):
                    res = self.readwrite(start, value, False)
                    success = 1
                else:
                    raise RuntimeError('Slice must have same length as data')
            except:
                print('Can only assign bytes/bytearray to a slice')
                success = 0
        return res



    def _rslice(self, addr):
        start, stop = self._do_slice(addr)
        buf = bytearray(stop - start)
        return self.readwrite(start, buf, True)


# A logical ferroelectric RAM made up of from 1 to 8 chips
class FRAM(BlockDevice):
    def __init__(self, i2c, verbose=True, block_size=9):
        self._i2c = i2c
        self._buf1 = bytearray(1)
        self._addrbuf = bytearray(2)  # Memory offset into current chip
        self._buf3 = bytearray(3)
        # self._nchips = self.scan(verbose, _SIZE)
        self._nchips = 1
        super().__init__(block_size, self._nchips, _SIZE)
        self._i2c_addr = 0x50  # None # i2c address of current chip

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
                self._i2c.readfrom_into(self._i2c_addr, mvb[start: start + npage])  # Sequential read
            else:
                self._i2c.writevto(self._i2c_addr, (self._addrbuf, buf[start: start + npage]))
            nbytes -= npage
            start += npage
            addr += npage
        return buf


# Return a FRAM array. Adapt for platforms other than Pyboard.
def get_fram(i2c):
    fram = FRAM(i2c)
    print('Instantiated FRAM')
    return fram


# -----------------------------------------------------------------------------------------------------------------#
# -----------------------------------------------------------------------------------------------------------------#
# -----------------------------------------------------------------------------------------------------------------#

def check(storage):
    for i in range(20):
        print(storage[i], end=" ")
    print("")
    return None


def get_locator(storage):
    return storage[0:2]


def locator_reset(storage):
    storage[0:2] = b'\x00\x02'
    return None


def bulk_reset(storage, amount):  # Max is 32
    for i in range(0, amount * 2):
        storage[i * 512:(i + 1) * 512] = b'\x00' * 512
        print(i * 512, (i + 1) * 512)
        locator_reset(storage)
    return None


def emergency_storage(storage, locator_byt, data):
    # Get FRAM Locator
    locator_int = int.from_bytes(locator_byt, "big")

    # Save Data to FRAM
    storage[locator_int:locator_int+9] = bytes(data[1:10])
    locator_int += 9

    # Update FRAM Locator
    locator_byt = locator_int.to_bytes(2, "big")
    storage[0:2] = locator_byt
    print('Loc:', locator_byt[0] * 256 + locator_byt[1])

    return locator_byt


def emergency_retrieve(storage, addr64, bn):
    # Get FRAM Locator
    locator_byt = storage[0:2]
    locator_int = int.from_bytes(locator_byt, "big")
    indexer = 2

    # Retrieve data from FRAM
    while indexer < locator_int:
        chunk = storage[indexer:indexer+9]
        for i in range(0, len(chunk)):
            if i == len(chunk) - 1:
                print(chunk[i])
            else:
                print(chunk[i], end=",")

        if sum(chunk) > 0:
            xbee.transmit(addr64, bytes([bn])+chunk)
            storage[indexer:indexer+9] = b'\x00' * 9
            time.sleep(1)
        indexer += 9

    # Reset FRAM board
    locator_reset(storage)


    # amount = locator_int // 1024 + 1
    # bulk_reset(storage, amount)

    return None
