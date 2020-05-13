/*C02 Sensor Controller.

This file defines a C02SensorController class that provides access to C02 sensor functionality.

This file is a part of the Wireless Sensor Network project.
(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
*/

#include "c02_sensor_controller.h"

#include <Arduino.h>
#include "debug_utils.h"


C02SensorController::C02SensorController(C02SensorModes mode) :
sensor(NDIR_I2C(I2C_ADDRESS)) {
    this->mode = mode;
}

bool C02SensorController::begin() {
    if (mode == C02SensorModes::MHZ16) {
        int attempts = 0;
        while (!sensor.begin()) {
            DEBUG_PRINT("MHZ16 failed to start");
            if (++attempts >= MAX_CONNECTION_ATTEMPTS) {
                DEBUG_PRINT("Max attempts reached. Aborting");
                return false;
            }
            delay(CONNECTION_ATTEMPT_DELAY);
        }
        DEBUG_PRINT("MHZ16 has started");
        return true;
    }

    return true;
}