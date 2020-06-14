/*CO2 Sensor Controller.

This file defines a CO2SensorController class that provides access to CO2 sensor functionality.

This file is a part of the Wireless Sensor Network project.
(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
*/

#include "CO2_sensor_controller.h"

#include <Arduino.h>
#include "debug_utils.h"


CO2SensorController::CO2SensorController(CO2SensorModes mode) :
sensor(NDIR_I2C(I2C_ADDRESS)) {
    this->mode = mode;
}


bool CO2SensorController::begin() {
    DEBUG_PRINTLN(F("Starting CO2 sensor controller"));

    if (mode == CO2SensorModes::MHZ16) {
        int attempts = 0;
        while (!sensor.begin()) {
            DEBUG_PRINTLN(F("MHZ16 failed to start"));
            if (++attempts >= MAX_CONNECTION_ATTEMPTS) {
                DEBUG_PRINTLN(F("Max attempts reached. Aborting"));
                return false;
            }
            delay(CONNECTION_ATTEMPT_DELAY);
        }
    }

    return true;
}


uint32_t CO2SensorController::collectData() {
    DEBUG_PRINTLN("Collecting data");

    if (mode == CO2SensorModes::FAKE_CONSTANT){
        return CONSTANT_VALUE;
    }
    
    if (mode == CO2SensorModes::FAKE_RANDOM){
        return 50;
    }
        
    else if (mode == CO2SensorModes::MHZ16) {
        if (sensor.measure())
            return sensor.ppm;
        else
            return 0;
    }
    
    else if (mode == CO2SensorModes::SEN0219) {

    }
    
    return 0;
}