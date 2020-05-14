/*Clock Controller.

This file defines a ClockController class that provides access to clock functionality.

This file is a part of the Wireless Sensor Network project.
(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
*/

#ifndef CLOCK_CONTROLLER_H
#define CLOCK_CONTROLLER_H

#include <RTClib.h>


enum class ClockModes {
  SIMULATED,
  RTC_DS3231
};


class ClockController {
    private:
        ClockModes mode;
        DateTime dt;
        RTC_DS3231 rtc;
        int MAX_CONNECTION_ATTEMPTS = 10;
        int CONNECTION_ATTEMPT_DELAY = 1000;

    public:
        ClockController(ClockModes mode);
        bool begin();
        int unixtime();
        bool isNextSecond();
        bool isNextMinute();
        bool isNextHour();
        bool isNextDay();
};


#endif
