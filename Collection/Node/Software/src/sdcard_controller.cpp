/*SD Card Controller.

This file defines a SDCardController class that provides access to SD Card functionality.

This file is a part of the Wireless Sensor Network project.
(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
*/

#include "sdcard_controller.h"

#include "debug_utils.h"
#include "data_utils.h"


SDCardController::SDCardController(SDCardModes mode) {
    this->mode = mode;
}


bool SDCardController::begin() {
    if (mode == SDCardModes::SD_FAT_ASCII || mode == SDCardModes::SD_FAT_BINARY) {
        int attempts = 0;
        while (!sd.begin(sdChipSelect)) {
            DEBUG_PRINT(F("SDFAT failed to start"));
            if (++attempts >= MAX_CONNECTION_ATTEMPTS) {
                DEBUG_PRINT(F("Max attempts reached. Aborting"));
                return false;
            }
            delay(CONNECTION_ATTEMPT_DELAY);
        }
    }

    DEBUG_PRINT(F("SD card controller has started"));
    return true;
}


bool SDCardController::writeDataPoint(uint32_t unixtime, uint32_t gasData) {
    uint32_t buffer[2] = {unixtime, gasData};
    checksum = crc32_bytes_update(checksum, buffer, sizeof(uint32_t)*2);

    if (mode == SDCardModes::SIMULATED_SERIAL) {
        Serial.print("<DataPoint: (");
        Serial.print(unixtime);
        Serial.print(", ");
        Serial.print(gasData);
        Serial.print(")>");
    }

    else if (mode == SDCardModes::SD_FAT_ASCII) {
        String line = String(unixtime) + "," + String(gasData);
        file.println(line);
        file.sync();
    }

    else if (mode == SDCardModes::SD_FAT_BINARY) {
        file.write(buffer, sizeof(uint32_t)*2);
        file.sync();
    }

    DEBUG_PRINT(F("Data point written"));

    return true;
}


bool SDCardController::createNewFile(char* filename) {
    DEBUG_PRINT(F("Creating new file"));

    if (mode == SDCardModes::SIMULATED_SERIAL) {
        Serial.print("<NewFileCreated: \"");
        Serial.print(filename);
        Serial.print("\">");
    }

    else if (mode == SDCardModes::SD_FAT_ASCII || mode == SDCardModes::SD_FAT_BINARY) {
        file.open(filename, O_CREAT|O_WRITE|O_APPEND);

        if (mode == SDCardModes::SD_FAT_ASCII)
            file.println("UNIXTIME,CO2");

        file.sync();
        DEBUG_PRINT("Created new file: " + String(filename));
    }

    return true;
}