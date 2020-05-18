/*Main.

This file is the main code to be run on each Node Module.

This file is a part of the Wireless Sensor Network project.
(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
*/

#ifndef UNIT_TEST


#include <Arduino.h>

#include "debug_utils.h"
#include "CO2_sensor_controller.h"
#include "clock_controller.h"
#include "sdcard_controller.h"
#include "data_utils.h"
#include "communication_controller.h"

#ifndef CLOCK_MODE
    #define CLOCK_MODE ClockModes::RTC_DS3231
#endif
#ifndef CO2_SENSOR_MODE
    #define CO2_SENSOR_MODE CO2SensorModes::MHZ16
#endif
#ifndef SDCARD_MODE
    #define SDCARD_MODE SDCardModes::SD_FAT_BINARY
#endif
#ifndef COMMUNICATION_MODE
    #define COMMUNICATION_MODE CommunicationModes::NRF24L01
#endif

ClockController clock(CLOCK_MODE);
CO2SensorController CO2Sensor(CO2_SENSOR_MODE);
SDCardController sdCard(SDCARD_MODE);
CommunicationController communication(COMMUNICATION_MODE);


void setup() {
    DEBUG_INIT();
    
    clock.begin();
    CO2Sensor.begin();
    sdCard.begin();
    communication.begin();

    DEBUG_PRINT(F("Finished setup()"));
}


void loop() {
    while(!clock.isNextSecond());

    uint32_t gasData = CO2Sensor.collectData();
    sdCard.writeDataPoint(clock.unixtime(), gasData);

    if (clock.isNextHour())
        sdCard.createNewFile(clock.currentFilename());

    if (clock.isNextDay())
        communication.sendFiles();
}


#endif