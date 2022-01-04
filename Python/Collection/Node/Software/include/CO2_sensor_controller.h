/*CO2 Sensor Controller.

This file defines a CO2SensorController class that provides access to CO2 sensor functionality.

This file is a part of the Wireless Sensor Network project.
(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
*/

#ifndef CO2_SENSOR_CONTROLLER_H
#define CO2_SENSOR_CONTROLLER_H

#include "NDIR_I2C.h"


enum class CO2SensorModes {
  FAKE_CONSTANT,
  FAKE_RANDOM,  // not yet implemented
  MHZ16,
  SEN0219  // not yet implemented
};


class CO2SensorController {
    private:
        const uint8_t I2C_ADDRESS = 0x4D;
        CO2SensorModes mode;
        NDIR_I2C sensor;
        int16_t MAX_CONNECTION_ATTEMPTS = 10;
        uint16_t CONNECTION_ATTEMPT_DELAY = 1000;
    public:
        CO2SensorController(CO2SensorModes mode);
        bool begin();
        uint32_t collectData();
        uint32_t CONSTANT_VALUE = 1;
};


#endif
