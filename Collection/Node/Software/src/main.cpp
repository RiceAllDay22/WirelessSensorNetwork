/*Main.

This file is the main code to be run on each Node Module.

This file is a part of the Wireless Sensor Network project.
(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
*/

#ifndef UNIT_TEST


#include <Arduino.h>

#define DEBUG
#define BAUD_RATE 9600

#include "debug_utils.h"

#include "c02_sensor_controller.h"
#include "clock_controller.h"
#include "sdcard_controller.h"
#include "data_utils.h"
#include "communication_controller.h"


#define CLOCK_MODE ClockModes::RTC_DS3231
#define C02_SENSOR_MODE C02SensorModes::MHZ16
#define SDCARD_MODE SDCardModes::SD_FAT
#define COMMUNICATION_MODE CommunicationModes::NRF24L01

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

    DEBUG_PRINT("Finished setup()");
}


void loop() {
    while(!clock.isNextSecond());

    DEBUG_PRINT("Collecting gas data");
    int gasData = c02Sensor.collectData();
    sdCard.writeDataPoint(clock.unixtime(), gasData);

    if (clock.isNextHour()) {
        DEBUG_PRINT("Creating new file");
        sdCard.createNewFile();
    }

    if (clock.isNextDay()) {
        DEBUG_PRINT("Sending files");
        communication.sendFiles();
    }
}


#endif