/*Main.

This file is the main code to be run on each Node Module.

This file is a part of the Wireless Sensor Network project.
(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
*/

#include <Arduino.h>

#include "c02_sensor_controller.h"
#include "clock_controller.h"
#include "sdcard_controller.h"
#include "data_utils.h"

#ifdef SIMULATE
  #define SIMULATE 0
#else
  #define SIMULATE 1
#endif

C02SensorController c02Sensor = C02SensorController(SIMULATE);
ClockController clock = ClockController(SIMULATE);
SDCardController sdCard = SDCardController(SIMULATE);


void setup() {

}


void loop() {

}
