/*Communications Controller.

This file defines a CommunicationsController class that provides acces to communications
functionality, such as sending and recieving data over a wireless network.

This file is a part of the Wireless Sensor Network project.
(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
*/

#include "communication_controller.h"

#include "debug_utils.h"


CommunicationController::CommunicationController(CommunicationModes mode) {
    this->mode = mode;
}


bool CommunicationController::begin() {
    DEBUG_PRINTLN(F("Starting communication controller"));
    return true;
}


bool CommunicationController::sendFiles() {
    DEBUG_PRINT("Sending files");

    if (mode == CommunicationModes::NONE) {
        return true;
    }

    else if (mode == CommunicationModes::FAKE_SERIAL) {

    }

    else if (mode == CommunicationModes::NRF24L01) {

    }

    return true;
}