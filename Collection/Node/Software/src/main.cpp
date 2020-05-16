/*Main.

This file is the main code to be run on each Node Module.

This file is a part of the Wireless Sensor Network project.
(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
*/

#ifndef UNIT_TEST


#include <Arduino.h>

#include "debug_utils.h"
#include "c02_sensor_controller.h"
#include "clock_controller.h"
#include "sdcard_controller.h"
#include "data_utils.h"
#include "communication_controller.h"

#ifndef CLOCK_MODE
    #define CLOCK_MODE ClockModes::RTC_DS3231
#endif
#ifndef C02_SENSOR_MODE
    #define C02_SENSOR_MODE C02SensorModes::MHZ16
#endif
#ifndef SDCARD_MODE
    #define SDCARD_MODE SDCardModes::SD_FAT_BINARY
#endif
#ifndef COMMUNICATION_MODE
    #define COMMUNICATION_MODE CommunicationModes::NRF24L01
#endif

ClockController clock(CLOCK_MODE);
C02SensorController c02Sensor(C02_SENSOR_MODE);
SDCardController sdCard(SDCARD_MODE);
CommunicationController communication(COMMUNICATION_MODE);


void setup() {
    DEBUG_INIT();
    
    clock.begin();
    c02Sensor.begin();
    sdCard.begin();
    communication.begin();

    DEBUG_PRINT(F("Finished setup()"));
}


void loop() {
    while(!clock.isNextSecond());

    uint32_t gasData = c02Sensor.collectData();
    sdCard.writeDataPoint(clock.unixtime(), gasData);

    if (clock.isNextHour())
        sdCard.createNewFile(clock.currentFilename());

    if (clock.isNextDay())
        communication.sendFiles();
}


#endif