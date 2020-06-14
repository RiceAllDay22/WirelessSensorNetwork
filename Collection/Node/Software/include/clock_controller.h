/*Clock Controller.

This file defines a ClockController class that provides access to clock functionality.

This file is a part of the Wireless Sensor Network project.
(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
*/

#ifndef CLOCK_CONTROLLER_H
#define CLOCK_CONTROLLER_H

#include <RTClib.h>


enum class ClockModes {
  FAKE_FAST,
  FAKE_SERIAL,
  RTC_DS3231
};


class ClockController {
    private:
        ClockModes mode;
        DateTime dt;
        uint8_t prevSecond;
        uint8_t prevMinute;
        uint8_t prevHour;
        uint8_t prevDay;
        RTC_DS3231 rtc;
        int MAX_CONNECTION_ATTEMPTS = 10;
        int CONNECTION_ATTEMPT_DELAY = 1000;
        uint32_t simulationTicks;

        void fakeTick();

    public:
        ClockController(ClockModes mode);
        bool begin();
        void setTime(uint32_t unixtime);
        uint32_t unixtime();
        bool isNextSecond();
        bool isNextMinute();
        bool isNextHour();
        bool isNextDay();
        char* currentFilename();
        uint32_t MAX_FAKE_TICKS = 5;
};


#endif
