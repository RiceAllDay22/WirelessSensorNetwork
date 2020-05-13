/*SD Card Controller.

This file defines a SDCardController class that provides access to SD Card functionality.

This file is a part of the Wireless Sensor Network project.
(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
*/

#include "sdcard_controller.h"

#include "debug_utils.h"


SDCardController::SDCardController(SDCardModes mode) {
    this->mode = mode;
}

bool SDCardController::begin() {
    if (mode == SDCardModes::SD_FAT) {
        int attempts = 0;
        while (!sd.begin()) {
            DEBUG_PRINT("SDFAT failed to start");
            if (++attempts >= MAX_CONNECTION_ATTEMPTS) {
                DEBUG_PRINT("Max attempts reached. Aborting");
                return false;
            }
            delay(CONNECTION_ATTEMPT_DELAY);
        }
        DEBUG_PRINT("SDFAT has started");
        return true;
    }

    return true;
}