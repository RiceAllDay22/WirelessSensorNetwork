/*C02 Sensor Controller.

This file defines a C02SensorController class that provides access to C02 sensor functionality.

This file is a part of the Wireless Sensor Network project.
(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
*/

#ifndef C02_SENSOR_CONTROLLER_H
#define C02_SENSOR_CONTROLLER_H

#include "NDIR_I2C.h"


enum class C02SensorModes {
  SIMULATED,
  MHZ16,
  SEN0219
};


class C02SensorController {
    private:
        const uint8_t I2C_ADDRESS = 0x4D;
        C02SensorModes mode;
        NDIR_I2C sensor;
        int MAX_CONNECTION_ATTEMPTS = 10;
        int CONNECTION_ATTEMPT_DELAY = 1000;
    public:
        C02SensorController(C02SensorModes mode);
        bool begin();
};


#endif
