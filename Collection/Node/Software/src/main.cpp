/*Main.

This file is the main code to be run on each Node Module.

This file is a part of the Wireless Sensor Network project.
(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
*/

#include "c02_sensor_controller.h"
#include "clock_controller.h"
#include "sdcard_controller.h"
#include "data_utils.h"


C02SensorController c02Sensor;
ClockController clock;
SDCardController sdCard;

#ifdef NO_HARDWARE
  c02Sensor = C02SensorController(true);
  clock = ClockController(true);
  sdCard = SDCardController(true);
#else
  c02Sensor = C02SensorController();
  clock = ClockController();
  sdCard = SDCardController();
#endif


void setup() {

}


void loop() {

}
