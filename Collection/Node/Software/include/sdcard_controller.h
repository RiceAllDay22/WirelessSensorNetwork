/*SD Card Controller.

This file defines a SDCardController class that provides access to SD Card functionality.

This file is a part of the Wireless Sensor Network project.
(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
*/

#ifndef SDCARD_CONTROLLER_H
#define SDCARD_CONTROLLER_H

#include "SdFat.h"


enum class SDCardModes {
  SIMULATED_SERIAL,
  SIMULATED_EMULATED,
  SD_FAT_CSV,
  SD_FAT_BINARY
};


class SDCardController {
    private:
        SDCardModes mode;
        SdFat sd;
        SdFile file;
        const uint8_t sdChipSelect = SS;
        int MAX_CONNECTION_ATTEMPTS = 10;
        int CONNECTION_ATTEMPT_DELAY = 1000;
        uint32_t checksum = 0;
    public:
        SDCardController(SDCardModes mode);
        bool begin();
        bool writeDataPoint(uint32_t unixtime, uint32_t gasData);
        bool createNewFile(char* filename);
};


#endif