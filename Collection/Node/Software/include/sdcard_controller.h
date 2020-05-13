/*SD Card Controller.

This file defines a SDCardController class that provides access to SD Card functionality.

This file is a part of the Wireless Sensor Network project.
(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
*/

#ifndef SDCARD_CONTROLLER_H
#define SDCARD_CONTROLLER_H

#include "SdFat.h"


enum class SDCardModes {
  SIMULATED,
  SD_FAT
};


class SDCardController {
    private:
        SDCardModes mode;
        SdFat sd;
        int MAX_CONNECTION_ATTEMPTS = 10;
        int CONNECTION_ATTEMPT_DELAY = 1000;
    public:
        SDCardController(SDCardModes mode);
        bool begin();
};


#endif