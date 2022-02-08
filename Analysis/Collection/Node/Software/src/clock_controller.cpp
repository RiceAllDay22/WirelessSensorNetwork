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
    DEBUG_PRINTLN(F("Starting clock controller"));

    if (mode == ClockModes::RTC_DS3231) {
        int attempts = 0;
        while (!rtc.begin()) {
            DEBUG_PRINTLN(F("RTC_DS3231 failed to start"));
            if (++attempts >= MAX_CONNECTION_ATTEMPTS) {
                DEBUG_PRINTLN(F("Max attempts reached. Aborting"));
                return false;
            }
            delay(CONNECTION_ATTEMPT_DELAY);
        }
        dt = rtc.now();
    }

    else if (mode == ClockModes::FAKE_FAST) {
        dt = DateTime(0).unixtime();
    }

    prevSecond = dt.second();
    prevMinute = dt.minute();
    prevHour = dt.hour();
    prevDay = dt.day();
    
    return true;
}


void ClockController::fakeTick() {
    if (mode == ClockModes::FAKE_FAST) {
        simulationTicks++;
        if (simulationTicks >= MAX_FAKE_TICKS) {
            simulationTicks = 0;
            dt = DateTime(dt.unixtime() + 1);
        }
    }

    else if (mode == ClockModes::FAKE_SERIAL) {
        if (Serial.available()) {
            if (Serial.read() == '\n') {
                dt = DateTime(dt.unixtime() + 1);
            }
        }
    }
}


void ClockController::setTime(uint32_t unixtime) {
    dt = DateTime(unixtime);

    if (mode == ClockModes::RTC_DS3231) {
        rtc.adjust(dt);
    }

    prevSecond = dt.second();
    prevMinute = dt.minute();
    prevHour = dt.hour();
    prevDay = dt.day();
}


uint32_t ClockController::unixtime() {
    return dt.unixtime();
}


bool ClockController::isNextSecond() {
    fakeTick();
    if (dt.second() != prevSecond) {
        prevSecond = dt.second();
        return true;
    }

    return false;
}


bool ClockController::isNextMinute() {
    fakeTick();
    if (dt.minute() != prevMinute) {
        prevMinute = dt.minute();
        return true;
    }

    return false;
}


bool ClockController::isNextHour() {
    fakeTick();
    if (dt.hour() != prevHour) {
        prevHour = dt.hour();
        return true;
    }

    return false;
}


bool ClockController::isNextDay() {
    fakeTick();
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