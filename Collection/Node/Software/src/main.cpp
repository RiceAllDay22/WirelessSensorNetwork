/*Main.

This file is the main code to be run on each Node Module.

This file is a part of the Wireless Sensor Network project.
(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
*/

#include <Arduino.h>

#define DEBUG
#define BAUD_RATE 9600

#include "c02_sensor_controller.h"
#include "clock_controller.h"
#include "sdcard_controller.h"
#include "data_utils.h"
#include "communication_controller.h"
#include "debug_utils.h"

#define CLOCK_MODE ClockModes::RTC_DS3231
#define C02_SENSOR_MODE C02SensorModes::MHZ16
#define SDCARD_MODE SDCardModes::SD_FAT
#define COMMUNICATION_MODE CommunicationModes::NRF24L01

ClockController clock(CLOCK_MODE);
C02SensorController c02Sensor(C02_SENSOR_MODE);
SDCardController sdCard(SDCARD_MODE);
CommunicationController communications(COMMUNICATION_MODE);


void setup() {
    DEBUG_INIT();

    clock.begin();
    c02Sensor.begin();
    sdCard.begin();
    communications.begin();
}


void loop() {
    
}
