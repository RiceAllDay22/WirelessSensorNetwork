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
            DEBUG_PRINT(F("RTC_DS3231 failed to start"));
            if (++attempts >= MAX_CONNECTION_ATTEMPTS) {
                DEBUG_PRINT(F("Max attempts reached. Aborting"));
                return false;
            }
            delay(CONNECTION_ATTEMPT_DELAY);
        }
        dt = rtc.now();
    }

    else if (mode == ClockModes::SIMULATED) {
        dt = DateTime(0, 0, 0, 0, 0, 0).unixtime();
    }

    prevSecond = dt.second();
    prevMinute = dt.minute();
    prevHour = dt.hour();
    prevDay = dt.day();

    DEBUG_PRINT(F("Clock controller has started"));
    return true;
}


void ClockController::simulationTick() {
    if (mode == ClockModes::SIMULATED) {
        simulationTicks++;
        if (simulationTicks >= MAX_SIMULATION_TICKS) {
            simulationTicks = 0;
            dt = DateTime(dt.unixtime() + 1);
        }
    }
}


int ClockController::unixtime() {
    simulationTick();
    return dt.unixtime();
}


bool ClockController::isNextSecond() {
    simulationTick();
    if (dt.second() != prevSecond) {
        prevSecond = dt.second();
        return true;
    }

    return false;
}


bool ClockController::isNextMinute() {
    simulationTick();
    if (dt.minute() != prevMinute) {
        return true;
    }

    return false;
}


bool ClockController::isNextHour() {
    simulationTick();
    if (dt.hour() != prevHour) {
        prevHour = dt.hour();
        return true;
    }

    return false;
}


bool ClockController::isNextDay() {
    simulationTick();
    if (dt.day() != prevDay) {
        prevDay = dt.day();
        return true;
    }

    return false;
}


char* ClockController::currentFilename() {
    char filename[19];
    sprintf(filename, "%04d-%02d-%02d--%02d.csv", dt.year(), dt.month(), dt.day(), dt.hour());
    return filename;
}