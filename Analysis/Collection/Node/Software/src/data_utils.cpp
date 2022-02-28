/*Data Utilities.

This file provides utility functions for reading, writing and verifying the integrity of binary
files generated by the sensor network. Files are in a custom binary format.

This file is a part of the Wireless Sensor Network project.
(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
*/

#include "data_utils.h"

#include "avr/pgmspace.h"


const uint32_t PROGMEM crc_table[16] = {
    0x00000000, 0x1db71064, 0x3b6e20c8, 0x26d930ac,
    0x76dc4190, 0x6b6b51f4, 0x4db26158, 0x5005713c,
    0xedb88320, 0xf00f9344, 0xd6d6a3e8, 0xcb61b38c,
    0x9b64c2b0, 0x86d3d2d4, 0xa00ae278, 0xbdbdf21c
};


uint32_t crc32_update(uint32_t crc, uint8_t data)
{
    uint8_t tbl_idx;
    tbl_idx = crc ^ (data >> (0 * 4));
    crc = pgm_read_dword_near(crc_table + (tbl_idx & 0x0f)) ^ (crc >> 4);
    tbl_idx = crc ^ (data >> (1 * 4));
    crc = pgm_read_dword_near(crc_table + (tbl_idx & 0x0f)) ^ (crc >> 4);
    return crc;
}


uint32_t crc32_ascii(char *s)
{
    uint32_t crc = ~0L;
    while (*s)
        crc = crc32_update(crc, *s++);
    
    return ~crc;
}


uint32_t crc32_bytes_update(uint32_t crc, void* buffer, uint32_t length) {
    uint8_t *newBuffer = (uint8_t*)buffer;

    crc = ~crc;

    for(uint32_t i = 0; i < length; i++) {
        crc = crc32_update(crc, newBuffer[i]);
    }

    return ~crc;
}