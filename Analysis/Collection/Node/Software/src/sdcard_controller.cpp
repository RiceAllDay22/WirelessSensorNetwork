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
    DEBUG_PRINTLN(F("Starting SD card controller"));

    if (mode == SDCardModes::SD_FAT_CSV || mode == SDCardModes::SD_FAT_BINARY) {
        int attempts = 0;
        while (!sd.begin(sdChipSelect)) {
            DEBUG_PRINTLN(F("SDFAT failed to start"));
            if (++attempts >= MAX_CONNECTION_ATTEMPTS) {
                DEBUG_PRINTLN(F("Max attempts reached. Aborting"));
                return false;
            }
            delay(CONNECTION_ATTEMPT_DELAY);
        }
    }

    return true;
}


bool SDCardController::writeDataPoint(uint32_t unixtime, uint32_t gasData) {
    DEBUG_PRINTLN("Writing datapoint");

    uint32_t buffer[2] = {unixtime, gasData};
    uint32_t length = sizeof(uint32_t)*2;
    checksum = crc32_bytes_update(checksum, buffer, length);

    if (mode == SDCardModes::NONE) {
        return true;
    }

    else if (mode == SDCardModes::FAKE_SERIAL || PRINT_TO_SERIAL) {
        Serial.print("<DataPoint: (");
        Serial.print(unixtime);
        Serial.print(", ");
        Serial.print(gasData);
        Serial.print("), CRC32: 0x");
        Serial.print(checksum, HEX);
        Serial.println(">");
    }

    else if (mode == SDCardModes::SD_FAT_CSV) {
        file.println(String(unixtime) + "," + String(gasData));
        file.sync();
    }

    else if (mode == SDCardModes::SD_FAT_BINARY) {
        file.seekEnd(length);
        file.write(buffer, sizeof(uint32_t)*2);
        file.write(&checksum, sizeof(uint32_t));
        file.sync();
    }

    return true;
}


bool SDCardController::createNewFile(char* filename) {
    DEBUG_PRINT("Creating new file");

    checksum = 0;

    if (mode == SDCardModes::NONE) {
        return true;
    }

    else if (mode == SDCardModes::FAKE_SERIAL) {
        Serial.print("<NewFileCreated: \"");
        Serial.print(filename);
        Serial.print("\">");
    }

    else if (mode == SDCardModes::SD_FAT_CSV || mode == SDCardModes::SD_FAT_BINARY) {
        file.open(filename, O_CREAT|O_WRITE|O_APPEND);

        if (mode == SDCardModes::SD_FAT_CSV)
            file.println("UNIXTIME,CO2");

        file.sync();
        DEBUG_PRINT("Created new file: " + String(filename));
    }

    return true;
}


uint32_t SDCardController::fileSize() {
    return file.fileSize();
}