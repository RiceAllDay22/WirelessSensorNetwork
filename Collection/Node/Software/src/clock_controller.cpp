/*Clock Controller.

This file defines a ClockController class that provides access to clock functionality.

This file is a part of the Wireless Sensor Network project.
(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
*/

#include "clock_controller.h"

#include "debug_utils.h"


ClockController::ClockController(ClockModes mode) {
    this->mode = mode;
}

bool ClockController::begin() {
    if (mode == ClockModes::RTC_DS3231) {
        int attempts = 0;
        while (!rtc.begin()) {
            DEBUG_PRINT("RTC_DS3231 failed to start");
            if (++attempts >= MAX_CONNECTION_ATTEMPTS) {
                DEBUG_PRINT("Max attempts reached. Aborting");
                return false;
            }
            delay(CONNECTION_ATTEMPT_DELAY);
        }
        DEBUG_PRINT("RTC_DS3231 has started");
        return true;
    }

    return true;
}